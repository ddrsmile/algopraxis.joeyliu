# -*- coding: utf-8 -*-
from django.db.models import TextChoices
from rest_framework import exceptions, status


class ErrorCode(TextChoices):
    COMMON = '401a', 'COMMON AUTH FAIL'
    EXPIRED = '401b', 'Token Expired'
    INVALID = '401c', 'Token Invalid'


class InvalidToken(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Token is invalid'
    default_code = ErrorCode.INVALID
