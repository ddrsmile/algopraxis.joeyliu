# -*- coding: utf-8 -*-
from django.test import TestCase

from ..paginations import ProblemPageNumberPagination


class ProblemPageNumberPaginationTest(TestCase):

    def setUp(self) -> None:
        self.pagination = ProblemPageNumberPagination()
        self.pagination.page_size = 3
