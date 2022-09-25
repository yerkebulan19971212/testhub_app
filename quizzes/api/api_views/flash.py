from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from base.paginate import FlashCardsPaginate
from quizzes.models import Question, FlashCard
from quizzes.api.serializers import QuestionsSerializer, FlashCardsSerializer


class ListFlashCardsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionsSerializer
    queryset = Question.objects.all()
    pagination_class = FlashCardsPaginate

    def get_queryset(self):
        user = self.request.user
        lesson_id = int(self.request.query_params.get('lesson_id'))
        num_of_quest = int(self.request.query_params.get('num_of_quest', 10))
        query = self.queryset.filter(
            lesson_question_level__test_type_lesson__lesson=lesson_id,
        ).exclude(flash_cards__in=FlashCard.objects.filter(user=user))
        return query[:num_of_quest]


list_flash_card = ListFlashCardsView.as_view()


class CreateFlashCards(CreateAPIView):
    serializer_class = FlashCardsSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


create_flash_cards = CreateFlashCards.as_view()
