# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.core.cache import cache

from rest_framework import (
    exceptions,
    serializers
)

from .exceptions import (
    ErrorCode,
    InvalidToken
)
from .utils import (
    issue_token,
    verify_token
)


def get_token(user_id):
    payload = {
        'user_id': user_id,
    }
    return issue_token(payload, 'refresh', 86400), issue_token(payload, 'access', 300)


class TokenAcquireSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        auth_kwargs = {
            'username': attrs.get('username'),
            'password': attrs.get('password'),
            'request': self.context.get('request'),
        }

        user = authenticate(**auth_kwargs)

        if user is None or not user.is_active:
            raise exceptions.AuthenticationFailed(
                detail='No active user found with given credentials',
                code=ErrorCode.COMMON,
            )

        refresh, access = get_token(user.id)

        return {'refresh': refresh, 'access': access}


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh')
        payload = verify_token(refresh_token)
        token_type = payload.get('token_type')
        user_id = payload.get('user_id')
        if not token_type or token_type != 'refresh':
            raise InvalidToken(
                detail='Refresh token is required to refresh the tokens',
                code=ErrorCode.INVALID
            )

        if not user_id:
            raise InvalidToken(
                detail='No user information found in the given refresh token',
                code=ErrorCode.INVALID
            )

        refresh, access = get_token(user_id)
        return {'refresh': refresh, 'access': access}


class TokenInvalidateSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    def invalidate(self, token: str) -> None:
        payload = verify_token(token)
        timeout = payload.get('ttl')
        cache.set(payload['jti'], 1, timeout=timeout)

    def validate(self, attrs):
        self.invalidate(attrs.get('refresh'))
        self.invalidate(attrs.get('access'))
        return {}
