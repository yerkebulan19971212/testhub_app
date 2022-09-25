from rest_framework.generics import CreateAPIView
from quizzes.api.serializers import FlashCardsSerializer


class CreateFlashCards(CreateAPIView):
    serializer_class = FlashCardsSerializer


create_flash_cards = CreateFlashCards.as_view()
