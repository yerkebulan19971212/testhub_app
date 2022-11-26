from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from quizzes.api.serializers import (LessonSerializer,
                                     LessonWithTestTypeLessonSerializer)
from quizzes.filters import LessonFilter
from quizzes.models import Lesson, LessonGroup


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
    # permission_classes = (IsAuthenticated,)
    queryset = Lesson.objects.prefetch_related(
        'test_type_lessons',
        'test_type_lessons__test_type'
    ).all()
    serializer_class = LessonWithTestTypeLessonSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = LessonFilter

    def get_queryset(self):
        language = self.request.headers.get('language', 'kz')
        queryset = super().get_queryset().filter(
            test_type_lessons__language=language,
            test_type_lessons__main=False
        )
        return queryset

    def get(self, request, *args, **kwargs):
        data = self.list(request, *args, **kwargs).data
        for lesson in data:
            test_type_lesson_id = lesson.get('test_type_lesson_id')
            lesson_group = LessonGroup.objects\
                .prefetch_related('lesson_pairs')\
                .filter(lesson_pairs__lesson_id=test_type_lesson_id)
            lesson_pair_ids = []
            for lg in lesson_group:
                for lp in lg.lesson_pairs.all():
                    lesson_pair_ids.append(lp.lesson_id)
            if lesson_pair_ids:
                lesson_pair_ids = list(set(lesson_pair_ids))
                lesson_pair_ids.remove(test_type_lesson_id)
            lesson['lesson_pairs'] = lesson_pair_ids
        return Response(data, status=status.HTTP_200_OK)


lesson_list_variant = LessonListVariantView.as_view()
