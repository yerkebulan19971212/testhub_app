from rest_framework import generics
from rest_framework import status as sts
from rest_framework.response import Response

from quizzes.api.serializers import FavoritesSerializer, QuestionsSerializer
from quizzes.models import Favorite, Question


class CreateFavoriteQuestions(generics.CreateAPIView):
    serializer_class = FavoritesSerializer
    queryset = Favorite.objects.all()

    def post(self, request, *args, **kwargs):
        question = self.request.data.get('question', None)
        obj, status = self.queryset.get_or_create(
            question_id=question,
            user=self.request.user
        )
        if status is False:
            obj.is_favorite = not obj.is_favorite
            obj.save()
        return Response(
            {'success': True},
            status=sts.HTTP_201_CREATED
        )


create_favorite_questions = CreateFavoriteQuestions.as_view()


class ListFavoritesView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer

    def get_queryset(self):
        return self.queryset.filter(
            favorites__is_favorite=True,
            user=self.request.user
        )


list_favorites_questions = ListFavoritesView.as_view()
