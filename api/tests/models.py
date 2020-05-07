# -*- coding: utf-8 -*-
from django.db import models

from taggit.models import TaggedItemBase
from taggit.managers import TaggableManager


class TestModelTag(TaggedItemBase):
    content_object = models.ForeignKey('TagSerializerTestModel', on_delete=models.CASCADE)

    class Meta:
        db_table = 'test_model_tag'


class TagSerializerTestModel(models.Model):
    tags = TaggableManager(through=TestModelTag, blank=True)

    class Meta:
        db_table = 'tag_serializer_test'
