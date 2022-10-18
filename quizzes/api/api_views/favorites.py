from rest_framework import generics, status as sts
from rest_framework.response import Response

from quizzes.api.serializers import FavoritesSerializer
from quizzes.models import Favorite


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
            if obj.is_favorite:
                obj.is_favorite = False
            else:
                obj.is_favorite = True
            obj.save()
        return Response(
            {'success': True},
            status=sts.HTTP_201_CREATED
        )


create_favorite_questions = CreateFavoriteQuestions.as_view()


class ListFavoritesView(generics.ListAPIView):
    pass
