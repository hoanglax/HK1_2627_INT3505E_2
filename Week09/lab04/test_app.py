import unittest
from unittest.mock import patch

from app import app


class OrderRoutingTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def post_order(self, account_id, cohort=None, percent=5):
        headers = {} if cohort is None else {"X-Cohort": cohort}
        with patch.dict(app.config, V2_PERCENT=percent):
            return self.client.post("/orders", json={"account_id": account_id}, headers=headers)

    def assert_handler(self, response, version, account_id):
        status_code, status = (200, "accepted") if version == "v1" else (201, "created")
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.headers["X-Order-Handler"], version)
        self.assertEqual(response.json, {"account_id": account_id, "status": status})

    def test_cohort_routes_to_v2_even_at_zero_percent(self):
        for cohort in ("beta", "internal"):
            with self.subTest(cohort=cohort), patch("gateway.hashlib.md5") as md5:
                response = self.post_order("acct_1", cohort=cohort, percent=0)
                self.assert_handler(response, "v2", "acct_1")
                md5.assert_not_called()

    def test_allow_list_routes_to_v2_even_at_zero_percent(self):
        for account_id in ("acct_42", "acct_99"):
            with self.subTest(account_id=account_id), patch("gateway.hashlib.md5") as md5:
                response = self.post_order(account_id, cohort="public", percent=0)
                self.assert_handler(response, "v2", account_id)
                md5.assert_not_called()

    def test_default_rollout_is_deterministic(self):
        self.assertEqual(app.config["V2_PERCENT"], 5)
        for account_id, version in (("acct_1", "v1"), ("acct_72", "v2")):
            with self.subTest(account_id=account_id):
                for _ in range(2):
                    response = self.client.post("/orders", json={"account_id": account_id})
                    self.assert_handler(response, version, account_id)

    def test_bucket_boundary_and_rollout_limits(self):
        # acct_21 hashes to bucket 5.
        for percent, version in ((0, "v1"), (5, "v1"), (6, "v2"), (100, "v2")):
            with self.subTest(percent=percent):
                self.assert_handler(self.post_order("acct_21", percent=percent), version, "acct_21")

    def test_invalid_json(self):
        for body in ("{", "[]", "null"):
            with self.subTest(body=body):
                response = self.client.post("/orders", data=body, content_type="application/json")
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json, {"error": "Expected a JSON object"})
                self.assertNotIn("X-Order-Handler", response.headers)

    def test_missing_or_invalid_account(self):
        for data in ({}, {"account_id": ""}, {"account_id": "  "}, {"account_id": 42}):
            with self.subTest(data=data):
                response = self.client.post("/orders", json=data, headers={"X-Cohort": "beta"})
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json, {"error": "account_id must be a non-empty string"})
                self.assertNotIn("X-Order-Handler", response.headers)
