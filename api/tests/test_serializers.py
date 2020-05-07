# -*- coding: utf-8 -*-
import json

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from taggit.models import Tag

from ..serializers import (
    TagList,
    TagSerializerField,
)

from .models import TagSerializerTestModel
from .serializers import TagTestSerializer


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


class TagSerializerTest(TestCase):

    def test_tag_serialize_creation(self) -> None:
        req_data = {
            'tags': ['tag1', 'tag2']
        }

        serializer = TagTestSerializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        test_model = serializer.save()
        self.assertEqual(list(test_model.tags.names().order_by('name')), req_data['tags'])

    def test_tag_serialize_update(self) -> None:
        req_data = {
            'tags': ['tag2', 'tag3']
        }

        test_model = TagSerializerTestModel.objects.create()
        test_model.tags.add('tag1', 'tag2')
        serializer = TagTestSerializer(test_model, data=req_data)
        serializer.is_valid(raise_exception=True)
        test_model = serializer.save()
        self.assertEqual(list(test_model.tags.names().order_by('name')), req_data['tags'])
