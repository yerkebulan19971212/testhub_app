import django_filters
from django_filters import NumberFilter
from django_filters import rest_framework as filters

from quizzes.models import Question


class FlashCardFilter(django_filters.FilterSet):
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
