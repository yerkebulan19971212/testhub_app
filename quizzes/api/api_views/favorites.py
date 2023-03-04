from rest_framework import generics
from rest_framework import status as sts
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from base.paginate import SimplePagination
from quizzes.api.serializers import FavoritesSerializer, QuestionsSerializer
from quizzes.filters.question import FavoriteFilter
from quizzes.models import Favorite, Question


class CreateFavoriteQuestions(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavoritesSerializer
    queryset = Favorite.objects.all()

    def post(self, request, *args, **kwargs):
        question = self.request.data.get('question', None)
        favorite_type = self.request.data.get('favorite_type', None)

        obj, create_status = self.queryset.get_or_create(
            question_id=question,
            favorite_type=favorite_type,
            user=self.request.user
        )
        if create_status is False:
            obj.is_favorite = not obj.is_favorite
            obj.save()
        return Response(
            {'success': True},
            status=sts.HTTP_201_CREATED
        )


create_favorite_questions = CreateFavoriteQuestions.as_view()


class ListFavoritesView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.select_related(
        'lesson_question_level__question_level'
    ).all()
    serializer_class = QuestionsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavoriteFilter
    pagination_class = SimplePagination

    def get_queryset(self):
        return super().get_queryset().filter(
            favorites__is_favorite=True,
            favorites__user=self.request.user
        ).prefetch_related(
            'answers'
        )


list_favorites_questions = ListFavoritesView.as_view()
