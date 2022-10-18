import django_filters
from django_filters import rest_framework as filters

from quizzes.models import Tag


class TagFilter(django_filters.FilterSet):
    test_type_lesson = filters.NumberFilter(
        field_name="test_type_lesson", required=True)

    class Meta:
        model = Tag
        fields = ('test_type_lesson',)
