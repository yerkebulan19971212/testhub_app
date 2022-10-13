import django_filters
from django.db.models import Q
from django_filters import CharFilter, NumberFilter
from django_filters import rest_framework as filters

from accounts.models import User
from quizzes.models import Answer, Lesson, Question


class LessonFilter(django_filters.FilterSet):
    test_type = filters.NumberFilter(
        field_name="test_type_lessons__test_type", required=True)

    class Meta:
        model = Lesson
        fields = ('test_type',)
