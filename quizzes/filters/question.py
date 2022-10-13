import django_filters
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.db.models import Q
from django_filters import CharFilter, NumberFilter
from django_filters import rest_framework as filters

from accounts.models import User
from quizzes.models import Answer, Lesson, Question


class QuestionFilter(django_filters.FilterSet):
    lesson_id = filters.NumberFilter(
        field_name="lesson_question_level__test_type_lesson_id"
    )
    tag_id = filters.NumberFilter(field_name="tag_questions__tag_id")
    q = CharFilter(method='search_filter')

    class Meta:
        model = Question
        fields = (
            'lesson_id',
            'tag_id'
        )

    @staticmethod
    def search_filter(queryset, name, value):
        # value_name_last_name = value.split(" ")
        # query = self.request.GET.get("q")
        search_vector = SearchVector("question")
        search_query = SearchQuery(value)
        return queryset.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by("-rank")
