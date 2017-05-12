# -*- coding: utf-8 -*-
# Django modules
from django import forms
# App modules
from .models import Problem, Solution, TestCase
from parts.widgets import CodeTextWidget

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = [
            'prob_no',
            'title',
            'prob_content',
            'sol_method_name',
            'input_parser_type',
            'parse_as_type',
        ]

class SolutionForm(forms.ModelForm):
    code = forms.CharField(widget=CodeTextWidget())
    class Meta:
        model = Solution
        fields = [
            'lang_mode',
            'code',
        ]

    def __init__(self, *args, **kwargs):
        super(SolutionForm, self).__init__(*args, **kwargs)
        self.fields['lang_mode'].widget.attrs.update({'onchange': 'update_code_mode(this)'})

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = [
            'content',
        ]