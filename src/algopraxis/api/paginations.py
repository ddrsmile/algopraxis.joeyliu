from collections import OrderedDict

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

    def has_solution(self, problem):
        user_id = self.request.user.id
        for solution in problem['solutions']:
            if solution['user'] == user_id:
                return True
        return False

    def customize_data(self, data):
        for i, problem in enumerate(data):
            content = [(k, v) for k, v in problem.items()]
            content += [('has_solution', self.has_solution(problem))]
            problem = OrderedDict(content)
            data[i] = problem
        return data

    def get_paginated_response(self, data):
        output = {
            'next_page_num': self.page.number + 1 if self.page.number < self.page.paginator.num_pages else None,
            'previous_page_num': self.page.number - 1 if self.page.number > 1 else None,
            'current_page': self.page.number,
            'count': self.page.paginator.count,
            'page_range': self.get_page_range(self.page),
            'results': self.customize_data(data)
        }

        return Response(output)

    def get_page_range(self, page):
        start_index = max(1, page.number - 2)
        end_index = min(start_index + 4, page.paginator.num_pages)

        start_index = min(start_index, max(end_index - 4, 1))

        page_range = [i for i in range(start_index, end_index + 1)]
        return page_range