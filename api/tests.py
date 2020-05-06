# -*- coding: utf-8 -*-
import json
from django.test import TestCase

from django.db import models
from rest_framework.serializers import ModelSerializer
from taggit.models import Tag
from rest_framework.exceptions import ValidationError

from .models import (
    Problem,
)

from .serializers import (
    TagList,
    TagSerializerField,
    TagSerializer,
)


# models.py
class ProblemTest(TestCase):

    def test_problem_creation(self) -> None:
        problem = Problem.objects.create(
            title='test title',
            difficulty=1,
            parser_type=1,
            input_type=1,
        )
        self.assertEqual(problem.slug, 'test-title')


# serializers.py
class TagListTest(TestCase):

    def setUp(self) -> None:
        self.field = TagSerializerField()

    def test_tag_list(self) -> None:
        tag_list = TagList(['tag1'])
        self.assertEqual(tag_list + TagList(['tag2']), TagList(['tag1', 'tag2']))
        self.assertEqual(tag_list[0], 'tag1')
        self.assertEqual(str(tag_list), json.dumps(['tag1'], sort_keys=True, indent=4, separators=(',', ': ')))
        self.assertEqual(str(TagList(['tag1'], pretty_print=False)), json.dumps(['tag1']))


class TagSerializerFieldTest(TestCase):

    def setUp(self) -> None:
        self.field = TagSerializerField()

    def test_to_internal_value(self) -> None:
        self.assertEqual(self.field.to_internal_value([]), [])
        self.assertEqual(self.field.to_internal_value(['tag1', 'tag2']), ['tag1', 'tag2'])
        self.assertEqual(self.field.to_internal_value('["tag1", "tag2"]'), ['tag1', 'tag2'])
        self.assertRaises(ValidationError, self.field.to_internal_value, data='tag1')
        self.assertRaises(ValidationError, self.field.to_internal_value, data='{"tag":"tag1"}')
        self.assertRaises(ValidationError, self.field.to_internal_value, data='{tag1')

    def test_to_representation(self) -> None:
        expected = TagList(['tag1', 'tag2'], pretty_print=True)
        self.assertEqual(self.field.to_representation(TagList(['tag1', 'tag2'], pretty_print=True)),
                         expected)
        self.assertEqual(self.field.to_representation(['tag1', 'tag2']), expected)
        for tag in ['tag1', 'tag2']:
            Tag(name=tag).save()
        self.assertEqual(self.field.to_representation(Tag.objects.all()), expected)

        self.assertRaises(ValidationError, self.field.to_representation, value='["tag1", "tag2"]')
        self.assertRaises(ValidationError, self.field.to_representation, value='["tag1", "tag2"]')


# class TagSerializerTest(TestCase):
#
#     class TestModel(models.Model):
#         tags = TaggableManager()
#
#         class Meta:
#             abstract = True
#
#     class TagTestSerializer(TagSerializer, ModelSerializer):
#         tags = TagSerializerField()
#
#         class Meta:
#             model = TestModel
#
#     def test_tag_serialize(self) -> None:
#         tags = ['tag1', 'tag2']
#         serialize = TagSerializer(data={'tags': tags})
#         print(serialize.is_valid(raise_exception=True))
#         print(serialize.errors)
#         print(serialize.data)
