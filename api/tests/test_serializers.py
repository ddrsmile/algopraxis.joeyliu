# -*- coding: utf-8 -*-
import json

from django.db import (
    connection,
    models
)
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from taggit.models import (
    Tag,
    TaggedItemBase
)
from taggit.managers import TaggableManager

from ..serializers import (
    TagList,
    TagSerializerField,
    TagSerializer
)


class TestModelTag(TaggedItemBase):
    content_object = models.ForeignKey('TagSerializerTestModel', on_delete=models.CASCADE)

    class Meta:
        db_table = 'test_model_tag'
        managed = False


class TagSerializerTestModel(models.Model):
    tags = TaggableManager(through=TestModelTag, blank=True)

    class Meta:
        db_table = 'tag_serializer_test'
        managed = False


class TagTestSerializer(TagSerializer, ModelSerializer):
    tags = TagSerializerField()

    class Meta:
        model = TagSerializerTestModel
        fields = '__all__'


class TagListTest(TestCase):

    def test_tag_list(self) -> None:
        tag_list = TagList(['tag1'])
        self.assertEqual(tag_list + TagList(['tag2']), TagList(['tag1', 'tag2']))
        self.assertEqual(tag_list[0], 'tag1')
        self.assertEqual(str(tag_list), json.dumps(['tag1'], sort_keys=True, indent=4, separators=(',', ': ')))
        self.assertEqual(str(TagList(['tag1'], pretty_print=False)), json.dumps(['tag1']))


class TagSerializerFieldTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super(TagSerializerFieldTest, cls).setUpClass()
        cls.field = TagSerializerField()

    @classmethod
    def tearDownClass(cls) -> None:
        super(TagSerializerFieldTest, cls).tearDownClass()

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

    @classmethod
    def setUpClass(cls) -> None:
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TagSerializerTestModel)
            schema_editor.create_model(TestModelTag)

    @classmethod
    def tearDownClass(cls) -> None:
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(TestModelTag)
            schema_editor.delete_model(TagSerializerTestModel)

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
