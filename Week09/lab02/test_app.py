import unittest

from app import app


class HeaderVersionTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def assert_headers(self, response, served):
        self.assertIn("X-API-Version", response.vary)
        self.assertEqual(response.headers.get("X-API-Version-Served"), served)

    def test_v1(self):
        response = self.client.get("/users/1", headers={"X-API-Version": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "full_name": "Văn Nguyễn"})
        self.assert_headers(response, "1")

    def test_v2_date_and_default(self):
        for requested in ("2", "2024-06-20", None):
            with self.subTest(requested=requested):
                headers = {} if requested is None else {"X-API-Version": requested}
                response = self.client.get("/users/1", headers=headers)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, {
                    "id": 1,
                    "first_name": "Văn",
                    "last_name": "Nguyễn",
                    "email": "a@vnu.vn",
                })
                self.assert_headers(response, requested or "2")

    def test_unsupported_version(self):
        for requested in ("3", "2024-06-21", ""):
            with self.subTest(requested=requested):
                response = self.client.get("/users/1", headers={"X-API-Version": requested})
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json, {"error": "Unsupported API version"})
                self.assert_headers(response, None)

    def test_user_not_found(self):
        response = self.client.get("/users/999", headers={"X-API-Version": "1"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "User not found"})
        self.assert_headers(response, "1")

    def test_decorator_preserves_view_name(self):
        self.assertEqual(app.view_functions["get_user"].__name__, "get_user")
