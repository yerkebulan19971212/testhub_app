import django_filters

from quizzes.models import InfoError


class InfoFilterByGradeType(django_filters.FilterSet):

    class Meta:
        model = InfoError
        fields = (
            'grade_type',
        )
