from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from quizzes.api.serializers import LessonSerializer
from quizzes.filters import LessonFilter
from quizzes.models import Lesson


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonFilter


lesson_list = LessonListView.as_view()
