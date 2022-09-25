import django_filters
from quizzes.models import Tag


class TagFilter(django_filters.FilterSet):
    class Meta:
        model = Tag
        fields = ('test_type_lesson',)
