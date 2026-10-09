import json
import os
import unittest
from unittest.mock import patch

from scripts.facebook_page_drafts import create_draft, list_drafts


class Response:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.payload


class FacebookPageDraftTests(unittest.TestCase):
    def test_create_draft_sends_unpublished_flag_and_bearer_token(self):
        captured = {}

        def intercepted_urlopen(request, timeout):
            captured["url"] = request.full_url
            captured["body"] = request.data.decode("utf-8")
            captured["authorization"] = request.get_header("Authorization")
            captured["timeout"] = timeout
            return Response({"id": "post-id"})

        with patch.dict(os.environ, {"META_PAGE_ID": "page-id", "META_PAGE_ACCESS_TOKEN": "page-token"}, clear=False):
            with patch("scripts.facebook_page_drafts.urlopen", intercepted_urlopen):
                result = create_draft("operator-approved-content")

        self.assertEqual(result, {"id": "post-id"})
        self.assertIn("published=false", captured["body"])
        self.assertIn("message=operator-approved-content", captured["body"])
        self.assertEqual(captured["authorization"], "Bearer page-token")
        self.assertNotIn("page-token", captured["url"])
        self.assertEqual(captured["timeout"], 30)

    def test_list_drafts_requests_unpublished_page_feed(self):
        captured = {}

        def intercepted_urlopen(request, timeout):
            captured["url"] = request.full_url
            captured["authorization"] = request.get_header("Authorization")
            return Response({"data": []})

        with patch.dict(os.environ, {"META_PAGE_ID": "page-id", "META_PAGE_ACCESS_TOKEN": "page-token"}, clear=False):
            with patch("scripts.facebook_page_drafts.urlopen", intercepted_urlopen):
                result = list_drafts()

        self.assertEqual(result, {"data": []})
        self.assertIn("is_published=false", captured["url"])
        self.assertIn("fields=id%2Cmessage%2Ccreated_time", captured["url"])
        self.assertEqual(captured["authorization"], "Bearer page-token")
        self.assertNotIn("page-token", captured["url"])


if __name__ == "__main__":
    unittest.main()
