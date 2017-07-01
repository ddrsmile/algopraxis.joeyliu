from django.shortcuts import get_object_or_404

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)

from algopraxis.api.permissons import IsOwnerOrReadOnly
from algopraxis.api.paginations import ProblemLimitOffsetPagination, ProblemPageNumberPagination
from algopraxis.models import Problem, Solution
from algopraxis.api.serializers import (
    ProblemListSerializer,
    ProblemDetailSerializer,
    ProblemCreateUpdateSerializer,
    SolutionSerializer,
)

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

# Solution
class SolutionCreateAPIView(CreateAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        problem = get_object_or_404(Problem, slug=self.kwargs.get('slug'))
        user = self.request.user
        serializer.save(user=user, problem=problem)

class SolutionUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = SolutionSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        problems = Problem.objects.all()
        queryset = get_object_or_404(problems, slug=self.kwargs.get('slug'))
        return queryset

    def get_object(self):
        problem = self.get_queryset()
        solution = get_object_or_404(problem.solutions, user=self.request.user)
        return solution

    def perform_update(self, serializer):
        problem = get_object_or_404(Problem, slug=self.kwargs.get('slug'))
        user = self.request.user
        serializer.save(user=user, problem=problem)

class SolutionDetailAPIView(RetrieveAPIView):
    serializer_class = SolutionSerializer
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
            solution = Solution(lang_mode='python3', code=problem.solution_start_code)
        return solution