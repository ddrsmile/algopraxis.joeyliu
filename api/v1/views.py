# -*- coding: utf-8 -*-
from django.db.utils import IntegrityError
from rest_framework.generics import (
    get_object_or_404,
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

from ..models import (
    Problem,
    CodeSet,
    Solution
)
from .paginations import ProblemPageNumberPagination
from .serializers import (
    ProblemCreateSerializer,
    ProblemSerializer,
    ProblemDetailSerializer,
    CodeSetCreateSerializer,
    CodeSetSerializer,
    SolutionCreateSerializer,
    SolutionSerializer,
    ExecutorSerializer
)


class ProblemCreateAPIView(CreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemCreateSerializer


class ProblemRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class ProblemListAPIView(ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    pagination_class = ProblemPageNumberPagination


class ProblemDetailAPIView(RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CodeSetCreateAPIView(CreateAPIView):
    serializer_class = CodeSetCreateSerializer

    def get_queryset(self):
        pass

    def perform_create(self, serializer):
        problem = get_object_or_404(Problem, id=self.request.data.get('problem_id'))
        try:
            serializer.save(problem=problem)
        except IntegrityError:
            # TODO: standardize the error code and error message.
            raise ValidationError('IntegrityError')


class CodeSetRUDAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CodeSetSerializer
    queryset = CodeSet.objects.all()


class SolutionCreateAPIView(CreateAPIView):
    serializer_class = SolutionCreateSerializer

    def get_queryset(self):
        pass

    def perform_create(self, serializer):
        problem = get_object_or_404(Problem, id=self.request.data.get('problem_id'))
        try:
            serializer.save(problem=problem, user=self.request.user)
        except IntegrityError:
            # TODO: standardize the error code and error message.
            raise ValidationError('IntegrityError')


class SolutionRUDAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()


class ExecuteAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ExecutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        problem = get_object_or_404(Problem, id=serializer.data.get('problem_id'))
        return Response({'problem': problem.id, 'data': serializer.data})
