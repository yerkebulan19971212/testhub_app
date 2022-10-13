from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from base.paginate import SimplePagination
from quizzes.api.serializers import QuestionsSerializer
from quizzes.filters import QuestionFilter
from quizzes.models import Question, Answer


class QuestionsListView(generics.ListAPIView):
    queryset = Question.objects.all().order_by('-id')[:20]
    serializer_class = QuestionsSerializer


questions_list = QuestionsListView.as_view()


class QuestionsListWithOnlyCorrectAnswerView(generics.ListAPIView):
    queryset = Question.objects.all().prefetch_related()
    serializer_class = QuestionsSerializer
    pagination_class = SimplePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionFilter

    def get_queryset(self):
        answers = Answer.objects.filter(correct=True)
        return super().get_queryset().\
            prefetch_related(Prefetch('answers', queryset=answers))


questions_list_with_only_correct_answer = QuestionsListWithOnlyCorrectAnswerView.as_view()
