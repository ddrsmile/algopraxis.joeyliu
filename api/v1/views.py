# -*- coding: utf-8 -*-
import typing

from django.db.models import Model
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
from .permissons import IsOwnerOrReadOnly
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


def check_integrity(model: typing.Type[Model], **kwargs) -> None:
    if model.objects.filter(**kwargs).exists():
        raise ValidationError(f'Integrity Error of {model.__name__}')


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
    queryset = CodeSet.objects.all()

    def perform_create(self, serializer):
        problem = get_object_or_404(Problem, id=self.request.data.get('problem_id'))
        check_integrity(CodeSet, problem_id=problem.id, lang_mode=serializer.validated_data.get('lang_mode'))
        serializer.save(problem=problem)


class CodeSetRUDAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CodeSetSerializer
    queryset = CodeSet.objects.all()


class SolutionCreateAPIView(CreateAPIView):
    serializer_class = SolutionCreateSerializer
    queryset = Solution.objects.all()


class SolutionRUDAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()


class ExecuteAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ExecutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        problem = get_object_or_404(Problem, id=serializer.data.get('problem_id'))
        return Response({'problem': problem.id, 'data': serializer.data})
