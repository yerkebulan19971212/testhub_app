from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from quizzes.api.serializers import GetLessonTestTypeLessonSerializer
from quizzes.filters import LessonFilter
from quizzes.models import TestTypeLesson


class GetLessonTestTypeLessonsView(generics.ListAPIView):
    queryset = TestTypeLesson.objects.all()
    serializer_class = GetLessonTestTypeLessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonFilter


get_lesson_test_type_lesson_view = GetLessonTestTypeLessonsView.as_view()
