# -*- coding: utf-8 -*-
# Django modules
from django import forms
# App modules
from .models import Problem, Solution
from parts.widgets import CodeTextWidget

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = [
            'title',
            'difficulty',
            'content',
            'main_file_code',
            'solution_start_code',
            'default_testcase',
            'tags',
        ]

    def __init__(self, *args, **kwargs):
        super(ProblemForm, self).__init__(*args, **kwargs)

        for _, field_item in self.fields.items():
            field_item.widget.attrs.update({'class': 'form-control'})

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
        self.fields['lang_mode'].widget.attrs.update({'onchange': 'update_code_mode(this)',
                                                      'class': 'form-control'})