import django_filters
from django.db.models import Q
from django_filters import CharFilter, NumberFilter
from django_filters import rest_framework as filters

from accounts.models import User
from quizzes.models import Answer, Lesson, Question, TestTypeLesson


class LessonFilter(django_filters.FilterSet):
    class Meta:
        model = TestTypeLesson
        fields = ('test_type',)
