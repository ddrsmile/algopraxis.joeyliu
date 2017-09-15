from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.http import Http404

class CreateUpdateModelMixin(object):

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {}
        for field in self.lookup_fields:
            filter_kwargs[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def create_or_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except Http404:
            instance = None

        if not instance:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()