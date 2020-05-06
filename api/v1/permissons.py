# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object'
    allow_methods = ('GET', 'PUT', 'POST', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):
        return request.method in self.allow_methods

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
