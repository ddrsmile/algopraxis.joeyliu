# -*- coding: utf-8 -*-
from typing import Optional

from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .exceptions import (
    ErrorCode,
)

from .utils import (
    verify_token
)

User = get_user_model()


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request) -> Optional[User]:
        token = self.get_token(request)
        if not token:
            return None, {}

        user_id = self.verify(token)
        return self.get_user(user_id), {'user_id': user_id}

    def authenticate_header(self, request):
        return 'Bearer ream="api"'

    def get_token(self, request) -> str:
        header = request.META.get('HTTP_AUTHORIZATION', '')
        if not header:
            return ''
        items = header.split()
        if len(items) != 2:
            raise AuthenticationFailed(
                detail='Authorization header must contain two space-delimited values',
                code=ErrorCode.COMMON
            )
        return items[1]

    def verify(self, token: str) -> dict:
        payload = verify_token(token)
        return payload.get('user_id')

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)
