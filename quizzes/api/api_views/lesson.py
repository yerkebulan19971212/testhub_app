from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from quizzes.api.serializers import LessonSerializer
from quizzes.models import Lesson
from quizzes.filters import LessonFilter


class LessonByTestType(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonFilter


lesson_by_test_type = LessonByTestType.as_view()
