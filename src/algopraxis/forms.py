# -*- coding: utf-8 -*-
# Django modules
from django import forms
# App modules
from .models import Problem, Solution, TestCase
from src.parts.widgets import CodeTextWidget
from . import LANG_MODE

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = [
            'prob_no',
            'prob_title',
            'prob_content',
            'sol_method_name',
            'input_parser_type',
            'parse_as_type',
        ]

class SolutionForm(forms.ModelForm):
    content = forms.CharField(widget=CodeTextWidget())
    class Meta:
        model = Solution
        fields = [
            'lang_mode',
            'content',
        ]

    def __init__(self, *args, **kwargs):
        super(SolutionForm, self).__init__(*args, **kwargs)
        self.lang_mode.widget.attrs.update({'onchange': 'update_code_mode(this)'})

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = [
            'content',
        ]