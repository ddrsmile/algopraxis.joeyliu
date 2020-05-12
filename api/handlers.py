# -*- coding: utf-8 -*-
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def exc_handler(exc, context):
    resp = exception_handler(exc, context)
    if isinstance(exc, APIException):
        resp.data = exc.get_full_details()
    return resp
