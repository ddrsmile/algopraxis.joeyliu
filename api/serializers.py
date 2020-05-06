# -*- coding: utf-8 -*-
import json

from django.db.models.query import QuerySet
from rest_framework import serializers


class TagList(list):

    def __init__(self, *args, **kwargs):
        pretty_print = kwargs.pop("pretty_print", True)
        list.__init__(self, *args, **kwargs)
        self.pretty_print = pretty_print

    def __add__(self, rhs):
        return TagList(list.__add__(self, rhs))

    def __getitem__(self, item):
        return list.__getitem__(self, item)

    def __str__(self):
        if self.pretty_print:
            return json.dumps(self, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            return json.dumps(self)


class TagSerializerField(serializers.Field):
    child = serializers.CharField()
    default_error_messages = {
        'not_a_list': 'Expected a list of items but got type "{data_type}".',
        'invalid_json': 'Invalid json list. A tag list submitted in string form must be valid json.',
        'not_a_str': 'All list items must be of string type.',
        'unknown_data_type': 'Unknown data type ({data_type}) to serialize.'
    }

    def __init__(self, *args, **kwargs):
        pretty_print = kwargs.pop("pretty_print", True)
        style = kwargs.pop("style", {})
        kwargs["style"] = {'base_template': 'textarea.html'}
        kwargs["style"].update(style)
        super(TagSerializerField, self).__init__(*args, **kwargs)
        self.pretty_print = pretty_print

    def to_internal_value(self, data):

        if not data:
            data = []

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except ValueError:
                self.fail('invalid_json')

        if not isinstance(data, list):
            self.fail('not_a_list', data_type=type(data).__name__)

        for item in data:
            self.child.run_validation(item)

        return data

    def to_representation(self, value):
        if isinstance(value, TagList):
            return value
        elif isinstance(value, list):
            return self.to_representation(TagList(value, pretty_print=self.pretty_print))
        elif isinstance(value, QuerySet) or hasattr(value, 'all'):
            return self.to_representation([tag.name for tag in value.all()])
        else:
            self.fail('unknown_data_type', data_type=type(value).__name__)


class TagSerializer(serializers.Serializer):

    def create(self, validated_data):
        to_be_tagged, validated_data = self._pop_tags(validated_data)
        tag_object = super(TagSerializer, self).create(validated_data)

        return self._save_tags(tag_object, to_be_tagged)

    def update(self, instance, validated_data):
        to_be_tagged, validated_data = self._pop_tags(validated_data)
        tag_object = super(TagSerializer, self).update(instance, validated_data)

        return self._save_tags(tag_object, to_be_tagged)

    def _save_tags(self, tag_object, tags):
        for key in tags.keys():
            tag_values = tags.get(key)
            getattr(tag_object, key).set(*tag_values)

        return tag_object

    def _pop_tags(self, validated_data):
        to_be_tagged = {}
        for key, field in self.fields.items():
            if isinstance(field, TagSerializerField):
                if key in validated_data:
                    to_be_tagged[key] = validated_data.pop(key)

        return to_be_tagged, validated_data
