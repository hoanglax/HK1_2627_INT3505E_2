import unittest
from unittest.mock import patch

from app import app
from blueprints.user_data import USERS


class UserApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_v1(self):
        response = self.client.get("/api/v1/users/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "id": 1, "full_name": "Văn Nguyễn", "email": "a@vnu.vn"
        })
        self.assertEqual(response.headers["Sunset"], "Thu, 31 Dec 2026 23:59:59 GMT")
        self.assertEqual(response.headers["Deprecation"], "true")

    def test_get_v2(self):
        response = self.client.get("/api/v2/users/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "id": 1, "first_name": "Văn", "last_name": "Nguyễn", "email": "a@vnu.vn"
        })
        self.assertNotIn("Deprecation", response.headers)
        self.assertNotIn("Sunset", response.headers)

    def test_missing_user(self):
        for version in (1, 2):
            with self.subTest(version=version):
                response = self.client.get(f"/api/v{version}/users/999")
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.json, {"error": "nf"})
                if version == 1:
                    self.assertEqual(response.headers["Deprecation"], "true")
                    self.assertEqual(
                        response.headers["Sunset"], "Thu, 31 Dec 2026 23:59:59 GMT"
                    )

    def test_create_and_read_in_both_versions(self):
        data = {"first_name": "An ", "last_name": "Le", "email": "an@example.com"}
        with patch.dict(USERS):
            response = self.client.post("/api/v2/users/", json=data)
            self.assertEqual(response.status_code, 201)
            uid = response.json["id"]
            self.assertEqual(response.json, {**data, "id": uid, "first_name": "An"})
            v2 = self.client.get(f"/api/v2/users/{uid}")
            self.assertEqual(v2.status_code, 200)
            self.assertEqual(v2.json, response.json)
            v1 = self.client.get(f"/api/v1/users/{uid}")
            self.assertEqual(v1.status_code, 200)
            self.assertEqual(v1.json["full_name"], "An Le")

    def test_invalid_json(self):
        url = "/api/v2/users/"
        for body in ("{", "[]", "null"):
            with self.subTest(body=body):
                response = self.client.post(url, data=body, content_type="application/json")
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json, {"error": "invalid JSON"})

    def test_invalid_fields(self):
        valid = {"first_name": "An", "last_name": "Le", "email": "an@example.com"}
        before = set(USERS)
        for data in ({}, {**valid, "first_name": 7}, {**valid, "last_name": " "},
                     {**valid, "email": "invalid-email"}):
            with self.subTest(data=data):
                response = self.client.post("/api/v2/users/", json=data)
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.json)
        self.assertEqual(set(USERS), before)
