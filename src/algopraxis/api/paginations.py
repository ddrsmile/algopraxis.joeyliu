from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)

class ProblemLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 100

class ProblemPageNumberPagination(PageNumberPagination):
    page_size = 1

    def get_paginated_response(self, data):
        output = {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'current_page': self.page.number,
            'count': self.page.paginator.count,
            'page_range': self.get_page_range(self.page),
            'results': data
        }

        return Response(output)

    def get_page_range(self, page):
        start_index = max(1, page.number - 2)
        end_index = min(start_index + 4, page.paginator.num_pages)

        start_index = min(start_index, max(end_index - 4, 1))

        page_range = [i for i in range(start_index, end_index + 1)]
        return page_range