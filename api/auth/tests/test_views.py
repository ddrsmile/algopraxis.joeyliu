# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from ..exceptions import (
    ErrorCode
)
from ..utils import (
    issue_token,
    verify_token
)


class APIViewTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super(APIViewTest, cls).setUpClass()
        cls.client = APIClient()

    @classmethod
    def tearDownClass(cls) -> None:
        super(APIViewTest, cls).tearDownClass()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user')
        cls.user.set_password('user')
        cls.user.save()

    def test_token_acquire_api_view(self) -> None:
        resp = self.client.post(
            reverse('api:auth:token_acquire'),
            data={
                'username': 'user',
                'password': 'user'
            },
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        refresh = verify_token(resp.data.get('refresh'))
        access = verify_token(resp.data.get('access'))
        self.assertEqual(refresh.get('token_type'), 'refresh')
        self.assertEqual(refresh.get('user_id'), self.user.id)
        self.assertEqual(access.get('token_type'), 'access')
        self.assertEqual(access.get('user_id'), self.user.id)

    def test_token_acquire_api_view_fail(self) -> None:
        resp = self.client.post(
            reverse('api:auth:token_acquire'),
            data={
                'username': 'fake',
                'password': 'user1'
            },
            content_type='application/json'
        )
        self.assertEqual(resp.data.get('message'), 'No active user found with given credentials')
        self.assertEqual(resp.data.get('code'), ErrorCode.COMMON)

    def test_token_refresh_api_view(self) -> None:
        token = issue_token({'user_id': self.user.id}, token_type='refresh')
        resp = self.client.post(
            reverse('api:auth:token_refresh'),
            data={
                'refresh': token,
            },
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        refresh = verify_token(resp.data.get('refresh'))
        access = verify_token(resp.data.get('access'))
        self.assertEqual(refresh.get('token_type'), 'refresh')
        self.assertEqual(refresh.get('user_id'), self.user.id)
        self.assertEqual(access.get('token_type'), 'access')
        self.assertEqual(access.get('user_id'), self.user.id)

    def test_token_refresh_api_view_wrong_token_type(self) -> None:
        token = issue_token({'user_id': self.user.id}, token_type='access')
        resp = self.client.post(
            reverse('api:auth:token_refresh'),
            data={
                'refresh': token,
            },
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.data.get('code'), ErrorCode.INVALID)

    def test_token_refresh_api_view_fake_token(self) -> None:
        token = issue_token({'userId': self.user.id}, token_type='refresh')
        resp = self.client.post(
            reverse('api:auth:token_refresh'),
            data={
                'refresh': token,
            },
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.data.get('code'), ErrorCode.INVALID)

    def test_token_invalidate_api_view(self) -> None:
        refresh_token = issue_token({'user_id': self.user.id}, token_type='refresh')
        access_token = issue_token({'user_id': self.user.id}, token_type='access')
        resp = self.client.post(
            reverse('api:auth:token_invalidate'),
            data={
                'refresh': refresh_token,
                'access': access_token
            },
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 204)
