import logging

from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.exceptions import DoesNotExist
from base.paginate import SimplePagination
from quizzes.api.serializers import QuestionsSerializer
from quizzes.api.serializers.question import QuestionDetailSerializer, \
    FullTestQuestionSerializer
from quizzes.filters import QuestionFilter
from quizzes.filters.question import FullTestQuestionFilter
from quizzes.models import Answer, Question

logger = logging.getLogger(__name__)


class QuestionsListView(generics.ListAPIView):
    queryset = Question.objects.all().order_by('-id')[:20]
    serializer_class = QuestionsSerializer
    pagination_class = SimplePagination

    def get(self, request, *args, **kwargs):
        return Response({"detail": "OK"})
        message = {
            'message': "user visits index()"
        }
        raise DoesNotExist()
        logger.info(message)
        return self.list(request, *args, **kwargs)


questions_list = QuestionsListView.as_view()


class QuestionsListWithOnlyCorrectAnswerView(generics.ListAPIView):
    queryset = Question.objects.filter(answers__correct=True)
    serializer_class = QuestionsSerializer
    pagination_class = SimplePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionFilter

    def get_queryset(self):
        answers = Answer.objects.filter(correct=True)
        return super().get_queryset(). \
            prefetch_related(Prefetch('answers', queryset=answers))


questions_list_with_only_correct_answer = QuestionsListWithOnlyCorrectAnswerView.as_view()


class DetailInfoQuestionView(generics.RetrieveAPIView):
    serializer_class = QuestionDetailSerializer
    queryset = Question.objects.all()
    lookup_field = 'id'


detail_info_question = DetailInfoQuestionView.as_view()


class FullTestQuestionView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FullTestQuestionSerializer
    queryset = Question.objects.select_related(
        'lesson_question_level__question_level'
    ).prefetch_related('answers').all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FullTestQuestionFilter

    def get(self, request, *args, **kwargs):
        data = {}
        questions = self.list(request, *args, **kwargs).data
        data['questions'] = questions
        user_answers = []
        for q in questions:
            user_answers.append({
                "question": q.get('id'),
                "answers": [],
                "is_mark": False
            })
        data["user_answers"] = user_answers
        return Response(data, status=status.HTTP_200_OK)


full_test_question = FullTestQuestionView.as_view()
