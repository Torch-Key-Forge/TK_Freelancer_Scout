import io
import json
import unittest
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from freelancer_scout import FreelancerScout, PRODUCTION_API, ScoutConfig


class _Response:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return json.dumps({"status": "success", "result": {"projects": []}}).encode()


class ReadOnlyBoundaryTests(unittest.TestCase):
    def test_search_uses_get_and_the_active_projects_endpoint(self):
        observed = {}

        def opener(request, *, timeout):
            observed["method"] = request.get_method()
            observed["url"] = request.full_url
            observed["timeout"] = timeout
            return _Response()

        scout = FreelancerScout(
            ScoutConfig(token="test-token", api_base=PRODUCTION_API),
            opener=opener,
        )
        result = scout.search_active_projects("data extraction", limit=5)

        self.assertEqual("GET", observed["method"])
        self.assertIn("/projects/0.1/projects/active/", observed["url"])
        self.assertIn("query=data+extraction", observed["url"])
        self.assertIn("limit=5", observed["url"])
        self.assertEqual("success", result["status"])

    def test_unapproved_api_hosts_are_rejected(self):
        with self.assertRaises(ValueError):
            ScoutConfig(token="test-token", api_base="https://example.com/api")

    def test_result_limit_is_bounded(self):
        scout = FreelancerScout(ScoutConfig(token="test-token"), opener=lambda *_: None)
        with self.assertRaises(ValueError):
            scout.search_active_projects("python", limit=21)


if __name__ == "__main__":
    unittest.main()

