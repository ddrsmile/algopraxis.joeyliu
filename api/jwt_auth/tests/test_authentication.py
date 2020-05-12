# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import (
    TestCase,
    RequestFactory
)
from rest_framework.exceptions import AuthenticationFailed

from ..authentication import (
    JWTAuthentication
)
from ..exceptions import (
    InvalidToken
)
from ..utils import (
    issue_token,
)


class AuthenticationTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super(AuthenticationTest, cls).setUpClass()
        cls.auth = JWTAuthentication()
        cls.req_factory = RequestFactory()

    @classmethod
    def tearDownClass(cls) -> None:
        super(AuthenticationTest, cls).tearDownClass()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user')
        cls.user.set_password('user')
        cls.user.save()

    def test_authenticate_header(self):
        req = self.req_factory.get('test_path')
        self.assertEqual(self.auth.authenticate_header(req), 'Bearer ream="api"')

    def test_authentication(self):
        token = issue_token({'user_id': self.user.id}, token_type='access')
        req = self.req_factory.get('test_path', HTTP_AUTHORIZATION=f'Bearer {token}')
        user, auth = self.auth.authenticate(req)
        self.assertEqual(user, self.user)
        self.assertEqual(auth.get('user_id'), self.user.id)

    def test_authentication_without_token(self):
        req = self.req_factory.get('test_path')
        user, auth = self.auth.authenticate(req)
        self.assertEqual(user, None)
        self.assertEqual(auth, {})

    def test_authentication_with_invalid_header(self):
        req = self.req_factory.get('test_path', HTTP_AUTHORIZATION='Bearer.token')
        self.assertRaises(AuthenticationFailed, self.auth.authenticate, req)

    def test_authentication_with_invalid_token(self):
        req = self.req_factory.get('test_path', HTTP_AUTHORIZATION='Bearer invalid.token')
        self.assertRaises(InvalidToken, self.auth.authenticate, req)
