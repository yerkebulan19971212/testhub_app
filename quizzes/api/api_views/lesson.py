from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from quizzes.api.serializers import (LessonSerializer,
                                     LessonWithTestTypeLessonSerializer)
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

    def get_queryset(self):
        language = self.request.headers.get('language', 'kz')
        queryset = super().get_queryset().filter(
            test_type_lessons__language=language)
        return queryset


lesson_list_with_test_type_lesson_view = LessonListWithTestTypeLessonView.as_view()


class LessonListVariantView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    # serializer_class =
    pass


lesson_list_variant = LessonListVariantView.as_view()