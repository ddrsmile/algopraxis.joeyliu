# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer

from ..serializers import (
    TagSerializerField,
    TagSerializer,
)

from .models import TagSerializerTestModel


class TagTestSerializer(TagSerializer, ModelSerializer):
    tags = TagSerializerField()

    class Meta:
        model = TagSerializerTestModel
        fields = '__all__'
