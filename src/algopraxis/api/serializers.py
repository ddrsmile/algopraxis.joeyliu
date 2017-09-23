# -*- coding: utf-8 -*-
import json
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from algopraxis.models import Problem, Solution, CodeSet

class TagList(list):
    def __init__(self, *args, **kwargs):
        pretty_print = kwargs.pop("pretty_print", True)
        list.__init__(self, *args, **kwargs)
        self.pretty_print = pretty_print

    def __add__(self, rhs):
        return TagList(list.__add__(self, rhs))

    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        try:
            return TagList(result)
        except TypeError:
            return result

    def __str__(self):
        if self.pretty_print:
            return json.dumps(
                self, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            return json.dumps(self)


class TagSerializerField(serializers.Field):
    child = serializers.CharField()
    default_error_messages = {
        'not_a_list': _(
            'Expected a list of items but got type "{input_type}".'),
        'invalid_json': _('Invalid json list. A tag list submitted in string'
                          ' form must be valid json.'),
        'not_a_str': _('All list items must be of string type.')
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
            data = "[]"
        try:
            data = json.loads(data)
        except ValueError:
            self.fail('invalid_json')

        if not isinstance(data, list):
            self.fail('not_a_list', input_type=type(data).__name__)

        for item in data:
            self.child.run_validation(item)

        return data

    def to_representation(self, value):
        if not isinstance(value, TagList):
            if not isinstance(value, list):
                tags = value.all()
                value = [tag.name for tag in tags]
            value = TagList(value, pretty_print=self.pretty_print)

        return value

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

        return (to_be_tagged, validated_data)


class SolutionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = [
            'user',
            'id',
            'problem',
            'lang_mode',
            'code',
        ]

class SolutionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = [
            'lang_mode',
            'code',
        ]

class CodeSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSet
        fields = [
            'lang_mode',
            'main_code',
            'start_code',
        ]

class ProblemListSerializer(TagSerializer, serializers.ModelSerializer):
    tags = TagSerializerField()
    solutions = SolutionDetailSerializer(many=True)
    class Meta:
        model = Problem
        fields =[
            'id',
            'title',
            'slug',
            'difficulty',
            'get_abs_url',
            'tags',
            'solutions',
        ]

class ProblemDetailSerializer(TagSerializer, serializers.ModelSerializer):
    tags = TagSerializerField()
    codesets = CodeSetSerializer(many=True)
    solutions = SolutionDetailSerializer(many=True)
    class Meta:
        model = Problem
        fields =[
            'id',
            'title',
            'slug',
            'difficulty',
            'codesets',
            'get_markdown_content',
            'tags',
            'solutions',
            'default_testcase',
        ]

class ProblemCreateUpdateSerializer(TagSerializer, serializers.ModelSerializer):
    tags = TagSerializerField()
    codesets = CodeSetSerializer(many=True)
    class Meta:
        model = Problem
        fields =[
            'title',
            'difficulty',
            'content',
            'default_testcase',
            'tags',
            'get_abs_url',
            'codesets',
        ]