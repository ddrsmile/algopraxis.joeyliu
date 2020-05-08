# -*- coding: utf-8 -*-
from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class ProblemPageNumberPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.page.number + 1 if self.page.number < self.page.paginator.num_pages else None),
            ('prev', self.page.number - 1 if self.page.number > 1 else None),
            ('page_range', self.get_page_range()),
            ('results', data)
        ]))

    def get_page_range(self):
        start_index = max(1, self.page.number - 2)
        end_index = min(start_index + 4, self.page.paginator.num_pages)
        start_index = min(start_index, max(end_index - 4, 1))
        return [i for i in range(start_index, end_index + 1)]
