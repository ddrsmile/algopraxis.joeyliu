# -*- coding: utf-8 -*-
import json

from rest_framework import serializers
from ..models import (
    Problem,
    Solution,
    CodeSet,
    LangMode
)
from ..serializers import (
    TagSerializerField,
    TagSerializer
)


class SolutionCreateSerializer(serializers.ModelSerializer):
    problem_id = serializers.IntegerField(source='problem.id')

    class Meta:
        model = Solution
        fields = (
            'problem_id',
            'lang_mode',
            'code',
        )


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = (
            'id',
            'lang_mode',
            'code',
        )


class CodeSetCreateSerializer(serializers.ModelSerializer):
    problem_id = serializers.IntegerField(source='problem.id')

    class Meta:
        model = CodeSet
        fields = (
            'problem_id',
            'lang_mode',
            'start_code',
        )


class CodeSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodeSet
        fields = (
            'id',
            'lang_mode',
            'start_code',
        )


class ProblemCreateSerializer(TagSerializer, serializers.ModelSerializer):
    tags = TagSerializerField()

    class Meta:
        model = Problem
        fields = (
            'title',
            'slug',
            'difficulty',
            'description',
            'parser_type',
            'input_type',
            'test_case',
            'tags',
        )


class ProblemSerializer(TagSerializer, serializers.ModelSerializer):
    tags = TagSerializerField()

    class Meta:
        model = Problem
        fields = (
            'id',
            'title',
            'slug',
            'difficulty',
            'description',
            'parser_type',
            'input_type',
            'test_case',
            'tags',
        )


class ProblemDetailSerializer(TagSerializer, serializers.ModelSerializer):
    tags = TagSerializerField()
    solutions = serializers.SerializerMethodField()
    code_sets = CodeSetSerializer(many=True)

    class Meta:
        model = Problem
        fields = (
            'title',
            'slug',
            'difficulty',
            'description',
            'parser_type',
            'input_type',
            'test_case',
            'tags',
            'code_sets',
            'solutions',
        )

    def get_solutions(self, obj):
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None
        own_solutions = obj.solutions.filter(user=user).all()
        return SolutionSerializer(own_solutions, many=True).data


def raise_validation_error(detail=None, code=None):
    raise serializers.ValidationError(detail, code)


class ExecutorSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    lang_mode = serializers.IntegerField(
        validators=[
            lambda x: True if type(x) == int and x in LangMode else raise_validation_error('lang_mode error!')
        ]
    )
    code = serializers.CharField(allow_blank=True)
    inputs = serializers.CharField(allow_blank=True)

    class Meta:
        fields = (
            'problem_id',
            'lang_mode',
            'code',
            'inputs',
        )
