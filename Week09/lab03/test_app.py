from datetime import timedelta
import unittest
from unittest.mock import patch

from app import SUNSET_DATE, app
from sunset import deprecate_at


class SunsetTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def get_v1_at(self, now):
        with patch.dict(app.config, SUNSET_DEMO_NOW=now):
            with self.assertLogs(app.logger, level="WARNING") as logs:
                response = self.client.get("/api/v1/users")
        self.assertIn("Deprecated endpoint called: GET /api/v1/users", logs.output[0])
        self.assertEqual(response.headers["Sunset"], "Thu, 31 Dec 2026 23:59:59 GMT")
        self.assertEqual(response.headers["Deprecation"], "true")
        self.assertEqual(
            response.headers["Link"], '</api/v2/users>; rel="successor-version"'
        )
        return response

    def test_before_sunset(self):
        response = self.get_v1_at(SUNSET_DATE - timedelta(seconds=1))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"users": [{"id": 1, "full_name": "Văn Nguyễn"}]})

    def test_at_and_after_sunset(self):
        for offset in (0, 1):
            with self.subTest(offset=offset):
                response = self.get_v1_at(SUNSET_DATE + timedelta(seconds=offset))
                self.assertEqual(response.status_code, 410)
                self.assertEqual(response.json, {
                    "error": "Endpoint has been retired",
                    "sunset": "2026-12-31T23:59:59+00:00",
                    "replacement": "/api/v2/users",
                })

    def test_v2_remains_available(self):
        with patch.dict(app.config, SUNSET_DEMO_NOW=SUNSET_DATE + timedelta(seconds=1)):
            response = self.client.get("/api/v2/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, {"users": [{"id": 1, "first_name": "Văn", "last_name": "Nguyễn"}]}
        )
        for header in ("Sunset", "Deprecation", "Link"):
            self.assertNotIn(header, response.headers)

    def test_optional_replacement_and_skipped_view(self):
        @deprecate_at(SUNSET_DATE)
        def view():
            self.fail("The retired view should not run")

        with app.test_request_context("/deprecated"):
            with patch.dict(app.config, SUNSET_DEMO_NOW=SUNSET_DATE):
                with self.assertLogs(app.logger, level="WARNING"):
                    response = view()

        self.assertEqual(response.status_code, 410)
        self.assertNotIn("Link", response.headers)
        self.assertIsNone(response.get_json()["replacement"])
