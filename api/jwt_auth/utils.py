# -*- coding: utf-8 -*-
import jwt
import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.core.cache import cache

from .exceptions import (
    ErrorCode,
    InvalidToken
)


def issue_token(payload: dict, token_type: str, ttl: int = -1) -> str:
    payload['token_type'] = token_type
    if ttl >= 0:
        payload['exp'] = datetime.utcnow() + timedelta(seconds=ttl)
        payload['ttl'] = ttl
    payload['jti'] = uuid.uuid4().hex
    return jwt.encode(payload, settings.SECRET_KEY).decode('utf-8')


def verify_token(token) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        cached = cache.get(payload.get('jti'))
        if cached:
            raise InvalidToken(
                detail=f'The {payload["token_type"]} has been invalidated',
                code=ErrorCode.INVALID
            )
        return payload
    except jwt.ExpiredSignatureError as e:
        raise InvalidToken(
            detail=f'{str(e)}',
            code=ErrorCode.EXPIRED
        )
    except Exception as e:
        raise InvalidToken(
            detail=f'{str(e)}',
            code=ErrorCode.INVALID
        )
