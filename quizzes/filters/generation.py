import django_filters
from django_filters import rest_framework as filters

from quizzes.models import Topic


class TopicFilter(django_filters.FilterSet):
    test_type_lesson_id = filters.NumberFilter(field_name="test_type_lesson")

    class Meta:
        model = Topic
        fields = ('test_type_lesson_id',)
