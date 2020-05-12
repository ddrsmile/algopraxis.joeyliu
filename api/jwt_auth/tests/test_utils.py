# -*- coding: utf-8 -*-
import time
from unittest.mock import patch

from django.test import TestCase
from django.core.cache.backends.locmem import LocMemCache
from ..exceptions import (
    InvalidToken
)
from ..utils import (
    issue_token,
    verify_token,
)


class UtilsTest(TestCase):

    def test_issue_correctness(self) -> None:
        token = issue_token({'user_id': 1}, token_type='access', ttl=-1)
        payload = verify_token(token)
        self.assertTrue('jti' in payload)
        self.assertTrue('exp' not in payload)
        self.assertEqual(1, payload['user_id'])
        self.assertEqual('access', payload['token_type'])

    def test_issue_expiry(self) -> None:
        token = issue_token({'user_id': 1}, token_type='access', ttl=0)
        time.sleep(1)
        self.assertRaises(InvalidToken, verify_token, token=token)

    def test_verify_fail(self) -> None:
        self.assertRaises(InvalidToken, verify_token, token='fake.token.4test')

    @patch.object(target=LocMemCache, attribute='get', new=lambda *args, **kwargs: 1)
    def test_verify_with_invalidated_token(self):
        token = issue_token({'user_id': 1}, token_type='access', ttl=-1)
        self.assertRaises(InvalidToken, verify_token, token=token)
