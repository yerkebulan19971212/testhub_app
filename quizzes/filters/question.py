import django_filters
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django_filters import CharFilter, NumberFilter
from django_filters import rest_framework as filters

from quizzes.models import Question, Favorite


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


class QuestionByLessonFilterByEvent(django_filters.FilterSet):
    quiz_event_id = filters.NumberFilter(
        field_name="quiz_event_questions__quiz_event_id",
        required=True
    )

    class Meta:
        model = Question
        fields = (
            'quiz_event_id',
        )


class FullTestQuestionFilter(django_filters.FilterSet):
    lesson_id = filters.NumberFilter(
        field_name="lesson_question_level__test_type_lesson_id",
        required=True
    )
    user_variant_id = filters.NumberFilter(
        field_name="variant_questions__variant__user_variant__id",
        required=True
    )

    class Meta:
        model = Question
        fields = (
            'lesson_id',
            'user_variant_id'
        )


class FavoriteFilter(django_filters.FilterSet):
    favorite_type = filters.CharFilter(
        field_name='favorites__favorite_type'
    )

    class Meta:
        model = Question
        fields = (
            'favorite_type',
        )


class GenerateVariantQuestionFilter(django_filters.FilterSet):
    lesson_id = filters.NumberFilter(
        field_name="lesson_question_level__test_type_lesson_id",
        required=True
    )
    variant_id = filters.NumberFilter(
        field_name="variant_questions__variant__id",
        required=True
    )

    class Meta:
        model = Question
        fields = (
            'lesson_id',
            'variant_id'
        )