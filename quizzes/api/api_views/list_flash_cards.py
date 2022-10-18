from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from quizzes.api.serializers import QuestionsSerializer
from quizzes.filters import FlashCardFilter
from quizzes.models import Answer, Question


class ListFlashCardsView(ListAPIView):
    serializer_class = QuestionsSerializer
    queryset = Question.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlashCardFilter

    def get_queryset(self):
        answers = Answer.objects.filter(correct=True)
        return super().get_queryset(). \
            prefetch_related(Prefetch('answers', queryset=answers))


list_flash_card = ListFlashCardsView.as_view()
