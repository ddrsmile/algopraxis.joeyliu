# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
# Django
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from . import PARSER_TYPE, PARSE_AS_TYPE, LANG_MODE

# 3rd party
from markdown import markdown
from taggit.models import TaggedItemBase
from taggit.managers import TaggableManager

class CustomManager(models.Manager):
    def first(self, *args, **kwargs):
        qs = super(CustomManager, self).all()
        try:
            return qs[0]
        except IndexError:
            return None

class AbstractBase(models.Model):
    def __init__(self, *args, **kwargs):
        super(AbstractBase, self).__init__(*args, **kwargs)
    id = models.AutoField(primary_key=True)
    objects = CustomManager()

    class Meta:
        abstract = True

class ProblemTag(TaggedItemBase):
    content_object = models.ForeignKey('Problem')

class Problem(AbstractBase):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    prob_no = models.IntegerField(unique=True)
    prob_title = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(unique=True)
    prob_content = models.TextField()
    sol_method_name = models.CharField(max_length=255, blank=False)
    input_parser_type = models.IntegerField(choices=PARSER_TYPE, default=1)
    parse_as_type = models.IntegerField(choices=PARSE_AS_TYPE, default=1)
    tags = TaggableManager(through=ProblemTag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"No: {prob_no} - Title: {prob_title}".format(prob_no=self.prob_no, prob_title=self.prob_title)

    def get_abs_url(self):
        return reverse('problems:detail', kwargs={'slug': self.slug})

    def get_markdown_prob_content(self):
        extensions = ["markdown.extensions.extra", "codehilite"]
        marked_content = markdown(self.prob_content, extensions=extensions)
        return mark_safe(marked_content)

    class Meta:
        ordering = ['prob_no']

def create_slug(instance, new_slug=None):
    slug = new_slug or slugify(instance.title)
    qs = Problem.objects.order_by(id)
    exists = qs.filter(slug=slug).exists()
    if exists:
        # added instance's id to the slug if the slug is existing.
        new_slug = "{slug}-{num}".format(slug=slug, num=qs.last().id + 1)
        return create_slug(instance=instance, new_slug=new_slug)
    return slug

def pre_save_signal_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_signal_receiver, sender=Problem)

class Solution(AbstractBase):
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='solutions')
    lang_mode = models.CharField(max_length=20, choices=LANG_MODE, default='python')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return "Problem {prob_no}'s solution".format(prob_no=self.problem.prob_no)

class TestCase(AbstractBase):
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='testcases')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Problem {prob_no}'s test case".format(prob_no=self.problem.prob_no)

    class Meta:
        ordering = ['-created_at', '-updated_at']