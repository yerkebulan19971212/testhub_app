import django_filters
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django_filters import CharFilter, NumberFilter
from django_filters import rest_framework as filters

from quizzes.models import Question


class QuestionFilter(django_filters.FilterSet):
    lesson_id = filters.NumberFilter(
        field_name="lesson_question_level__test_type_lesson_id"
    )
    test_type_id = filters.NumberFilter(
        field_name="lesson_question_level__test_type_lesson__test_type_id",
        required=True
    )
    tag_id = filters.NumberFilter(field_name="tag_questions__tag_id")
    q = CharFilter(method='search_filter', required=True)

    class Meta:
        model = Question
        fields = (
            'lesson_id',
            'tag_id',
            'test_type_id'
        )

    @staticmethod
    def search_filter(queryset, name, value):
        search_vector = SearchVector("question")
        search_query = SearchQuery(value)
        return queryset.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by("-rank")


class QuestionByLessonFilter(django_filters.FilterSet):
    lesson_id = filters.NumberFilter(
        field_name="lesson_question_level__test_type_lesson_id",
        required=True
    )
    num_of_question = NumberFilter(method='limit_the_amount', required=True)

    class Meta:
        model = Question
        fields = (
            'lesson_id',
        )

    @staticmethod
    def limit_the_amount(queryset, name, value):
        return queryset[:value]
