# -*- coding: utf-8 -*-
from django.http import Http404
from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)

from algopraxis.models import Problem, CodeSet, Solution
from algopraxis.api.permissons import IsOwnerOrReadOnly, IsReadOnly
from algopraxis.api.paginations import ProblemPageNumberPagination
from algopraxis.api.mixins import CreateUpdateModelMixin
from algopraxis.api.serializers import (
    ProblemListSerializer,
    ProblemDetailSerializer,
    ProblemCreateUpdateSerializer,
    CodeSetSerializer,
    SolutionDetailSerializer,
    SolutionCreateUpdateSerializer,
)
from coderunner.tasks import run_codes

# common
class RetrieveCreateUpdateAPIView(RetrieveModelMixin ,CreateUpdateModelMixin, GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create_or_update(request, *args, **kwargs)


# Problem
class ProblemCreateAPIView(CreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ProblemDetailAPIView(RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def filter_solutions(self, solutions):
        user_id = self.request.user.id
        for solution in solutions:
            if solution['user'] == user_id:
                return solution
        return None

    def get_user_solutions(self, solutions):
        user_id = self.request.user.id
        user_solutions = []
        for solution in solutions:
            if solution['user'] == user_id:
                user_solutions.append(solution)
        return user_solutions

    def customize_data(self, data):
        solutions = self.filter_solutions(data.pop('solutions'))
        #user_solutions = self.get_user_solutions(data.pop('solutions'))
        data['solutions'] = solutions
        #data['user_solutions'] = user_solutions
        return data

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.solutions = instance.solutions.filter(user_id=self.request.user.id)
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)


class ProblemUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsAdminUser]

class ProblemDeleteAPIView(DestroyAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsAdminUser]

class ProblemListAPIView(ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemListSerializer
    permission_classes = [AllowAny]
    pagination_class = ProblemPageNumberPagination

# CodeSet
class CodeSetCreateUpdateAPIView(RetrieveCreateUpdateAPIView):
    queryset = CodeSet.objects.all()
    serializer_class = CodeSetSerializer
    lookup_field = 'lang_mode'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            problem_slug = self.kwargs.get('slug', None)
            queryset = queryset.filter(problem__slug=problem_slug).all()

        return queryset

    def perform_create(self, serializer):
        problem = get_object_or_404(Problem, slug=self.kwargs.get('slug'))
        serializer.save(problem=problem)

# Solution
class SolutionCreateAPIView(CreateAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        problem = get_object_or_404(Problem, slug=self.kwargs.get('slug'))
        user = self.request.user
        serializer.save(user=user, problem=problem)

class SolutionUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionCreateUpdateSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class SolutionCreateUpdateAPIView(RetrieveCreateUpdateAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionCreateUpdateSerializer
    lookup_field = 'lang_mode'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            problem_slug = self.kwargs.get('slug', None)
            queryset = queryset.filter(problem__slug=problem_slug).all()

        return queryset

    def perform_create(self, serializer):
        problem = get_object_or_404(Problem, slug=self.kwargs.get('slug'))
        user = self.request.user
        serializer.save(user=user, problem=problem)

class SolutionDetailAPIView(RetrieveAPIView):
    serializer_class = SolutionDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def get_queryset(self):
        problems = Problem.objects.all()
        queryset = get_object_or_404(problems, slug=self.kwargs.get('slug'))
        return queryset

    def get_object(self):
        problem = self.get_queryset()
        user_id = self.request.user.id
        solution = problem.solutions.filter(user_id=user_id).first()
        if not solution:
            solution = Solution(lang_mode='python', code=problem.solution_start_code)
        return solution

class RunAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, slug=None):
        try:
            problem = get_object_or_404(Problem, slug=slug)
            lang_mode = request.POST.get('lang_mode')
            sol = request.POST.get('code')
            testcase = request.POST.get('testcases')
            codeset = get_object_or_404(problem.codesets, lang_mode=lang_mode)
            main = codeset.main_code
        except Http404:
            return Response(["The problem ro the language mode can not be found!!"])
        except Exception as e:
            message = "An exception of type {0} occurred.\n {1}"
            return Response([message.format(type(e).__name__, str(e))])

        result = run_codes.delay(lang_mode, main, sol, testcase)
        outputs = result.get(timeout=5)
        #outputs = run_codes(lang_mode, main, sol, testcase)

        return Response(outputs)