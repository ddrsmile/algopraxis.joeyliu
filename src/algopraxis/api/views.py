from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
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

from algopraxis.api.permissons import IsOwnerOrReadOnly, IsReadOnly
from algopraxis.api.paginations import ProblemPageNumberPagination
from algopraxis.models import Problem, Solution
from algopraxis.api.serializers import (
    ProblemListSerializer,
    ProblemDetailSerializer,
    ProblemCreateUpdateSerializer,
    SolutionSerializer,
)

from coderunner.tasks import run_codes

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

    def customize_data(self, data):
        solution = self.filter_solutions(data.pop('solutions'))
        data['solution'] = solution
        return data

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = self.customize_data(serializer.data)

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
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

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

class RunAPIView(APIView):
    permission_classes = [IsReadOnly]

    def get(self, request, slug=None):
        problem = get_object_or_404(Problem, slug=slug)
        main_content = problem.main_file_code
        sol_content = request.GET.get('code')
        input_data = request.GET.get('testcases')
        ansyc_result = run_codes.delay(main_content, sol_content, input_data)
        outputs = ansyc_result.get()
        return Response(outputs)