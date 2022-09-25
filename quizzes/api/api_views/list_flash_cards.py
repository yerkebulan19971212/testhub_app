from rest_framework.generics import ListAPIView

from base.paginate import FlashCardsPaginate
from quizzes.models import Question, FlashCard
from quizzes.api.serializers import QuestionsSerializer


class ListFlashCardsView(ListAPIView):
    serializer_class = QuestionsSerializer
    queryset = Question.objects.all()
    pagination_class = FlashCardsPaginate

    def get_queryset(self):
        lesson_id = int(self.request.query_params.get('lesson_id'))
        num_of_quest = int(self.request.query_params.get('num_of_quest', 10))
        query = self.queryset.filter(
            lesson_question_level__test_type_lesson__lesson=lesson_id
        ).exclude(flashcard__in=FlashCard.objects.all())
        return query[:num_of_quest]


list_flash_card = ListFlashCardsView.as_view()
