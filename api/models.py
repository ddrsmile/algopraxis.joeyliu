# -*- coding: utf-8
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


# choice options
class Difficulty(models.IntegerChoices):
    EASY = 1, 'EASY'
    MEDIUM = 2, 'MEDIUM'
    HARD = 3, 'HARD'


class LangMode(models.IntegerChoices):
    PYTHON3 = 1, 'python3'
    JAVA = 2, 'java'


class InputType(models.IntegerChoices):
    INTEGER = 1, 'integer'
    FLOAT = 2, 'float'
    STRING = 3, 'string'


class ParserType(models.IntegerChoices):
    VALUE = 1, 'VALUE'
    LIST = 2, 'LIST'
    LISTS = 3, 'LISTS'
    MATRIX = 4, 'MATRIX'


class AbstractBase(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class AbstractTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProblemTag(TaggedItemBase):
    content_object = models.ForeignKey('Problem', on_delete=models.CASCADE)

    class Meta:
        db_table = 'problem_tag'


class Problem(AbstractBase, AbstractTimeStamp):
    title = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(db_index=True, unique=True)
    description = models.TextField(blank=True)
    difficulty = models.IntegerField(choices=Difficulty.choices, default=1)
    parser_type = models.IntegerField(choices=ParserType.choices)
    input_type = models.IntegerField(choices=InputType.choices)
    test_case = models.TextField(blank=True)
    tags = TaggableManager(through=ProblemTag, blank=True)

    class Meta:
        db_table = 'problem'
        ordering = ['id']


@receiver([pre_save], sender=Problem)
def problem_signal_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class CodeSet(AbstractBase, AbstractTimeStamp):
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='code_sets')
    lang_mode = models.IntegerField(choices=LangMode.choices)
    start_code = models.TextField(blank=True)

    class Meta:
        db_table = 'code_set'
        unique_together = (('problem', 'lang_mode'),)
        ordering = ['problem__id', 'lang_mode']


class Solution(AbstractBase, AbstractTimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='solutions')
    lang_mode = models.IntegerField(choices=LangMode.choices)
    code = models.TextField(blank=True)

    class Meta:
        db_table = 'solution'
        unique_together = (('user', 'problem', 'lang_mode'),)
        ordering = ['problem__id', '-updated_at', '-created_at']
