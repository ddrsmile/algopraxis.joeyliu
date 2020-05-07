# -*- coding: utf-8 -*-

from django.test import TestCase

from ..models import (
    Problem,
)


class ProblemTest(TestCase):

    def test_problem_creation(self) -> None:
        problem = Problem.objects.create(
            title='test title',
            difficulty=1,
            parser_type=1,
            input_type=1,
        )
        self.assertEqual(problem.slug, 'test-title')
