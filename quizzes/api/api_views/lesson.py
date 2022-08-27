from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from quizzes.api.serializers import LessonSerializer, \
    LessonWithTestTypeLessonSerializer
from quizzes.filters import LessonFilter
from quizzes.models import Lesson


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


lesson_list = LessonListView.as_view()


class LessonListWithTestTypeLessonView(generics.ListAPIView):
    queryset = Lesson.objects.prefetch_related(
        'test_type_lessons',
        'test_type_lessons__test_type'
    ).all()
    serializer_class = LessonWithTestTypeLessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonFilter


lesson_list_with_test_type_lesson_view = LessonListWithTestTypeLessonView.as_view()
