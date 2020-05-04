from django.contrib import admin
from .models import Problem
from .forms import ProblemForm


class ProblemModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at', 'created_at']
    list_display_links = ['updated_at']
    list_editable = ['title']
    list_filter = ['title', 'updated_at', 'created_at']
    search_fields = ['title', 'prob_content']
    form = ProblemForm

    class Meta:
        model = Problem


admin.site.register(Problem, ProblemModelAdmin)
