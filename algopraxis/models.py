# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from markdown import markdown
from taggit.models import TaggedItemBase
from taggit.managers import TaggableManager

# choice options
DIFFICULTY = (
    (1, 'EASY'),
    (2, 'MEDIUM'),
    (3, 'HARD')
)

PARSER_TYPE = (
    (1, 'INTEGER'),
    (2, 'FLOAT'),
    (3, 'STRING')
)

PARSING_METHOD = (
    (1, 'SINGLE VALUE'),
    (2, 'LIST'),
    (3, 'LISTS'),
    (4, 'MATRIX'),
)

EXTERNAL_OBJECT = (
    ('None', 'None'),
    ('ListNode', 'ListNode'),
    ('TreeNode', 'TreeNode'),
    ('Interval', 'Interval'),
)

LANG_MODE = (
    ('python', 'Python3'),
    ('java', 'Java'),
    ('c_cpp', 'C++'),
)


class CustomManager(models.Manager):
    def first(self):
        qs = super(CustomManager, self).all()
        try:
            return qs[0]
        except IndexError:
            return None


class AbstractBase(models.Model):
    def __init__(self, *args, **kwargs):
        super(AbstractBase, self).__init__(*args, **kwargs)
    objects = CustomManager()

    class Meta:
        abstract = True


class AbstractTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(AbstractTimeStamp, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True


class ProblemTag(TaggedItemBase):
    content_object = models.ForeignKey('Problem', on_delete=models.CASCADE)


class Problem(AbstractBase, AbstractTimeStamp):
    # basic information
    title = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(db_index=True, unique=True)
    difficulty = models.IntegerField(choices=DIFFICULTY, default=1)
    content = models.TextField()
    tags = TaggableManager(through=ProblemTag, blank=True)
    # testcase
    default_testcase = models.TextField()

    def __str__(self):
        return u"No: {id} - Title: {title}".format(id=self.id, title=self.title)

    def get_abs_url(self):
        return reverse('algopraxis:detail', kwargs={'slug': self.slug})

    def get_markdown_content(self):
        extensions = ["markdown.extensions.extra", "codehilite"]
        marked_content = markdown(self.content, extensions=extensions)
        return mark_safe(marked_content)

    def get_tags_list(self):
        return self.tags.values_list('name', flat=True)

    @property
    def get_difficulty(self):
        return DIFFICULTY[self.difficulty - 1][1]

    @property
    def has_solution(self):
        solutions = Solution.objects.filter(problem=self)
        return solutions.count() > 0

    class Meta:
        ordering = ['id']


def create_slug(instance, new_slug=None):
    slug = new_slug or slugify(instance.title)
    qs = Problem.objects.order_by("id")
    exists = qs.filter(slug=slug).exists()
    if exists:
        # added instance's id to the slug if the slug is existing.
        new_slug = "{slug}-{num}".format(slug=slug, num=qs.last().id + 1)
        return create_slug(instance=instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Problem)
def pre_save_signal_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


class CodeSet(AbstractBase, AbstractTimeStamp):
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='codesets')
    lang_mode = models.CharField(max_length=20, choices=LANG_MODE)
    main_code = models.TextField()
    start_code = models.TextField()

    class Meta:
        unique_together = (('problem', 'lang_mode'),)
        ordering = ['-updated_at', '-created_at']


class Solution(AbstractBase, AbstractTimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='solutions')
    lang_mode = models.CharField(max_length=20, choices=LANG_MODE, default='python')
    code = models.TextField()

    class Meta:
        unique_together = (('user', 'problem', 'lang_mode'),)
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return "Problem {id}'s solution".format(id=self.problem.id)
