# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..jwt_auth.authentication import (
    JWTAuthentication,
)

from .serializers import (
    TokenAcquireSerializer,
    TokenRefreshSerializer,
    TokenInvalidateSerializer
)


@api_view(['POST'])
def token_acquire_api_view(request, *args, **kwargs):
    serializer = TokenAcquireSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token_refresh_api_view(request, *args, **kwargs):
    serializer = TokenRefreshSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token_invalidate_api_view(request, *args, **kwargs):
    serializer = TokenInvalidateSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_204_NO_CONTENT)