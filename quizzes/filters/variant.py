import django_filters
from django_filters import rest_framework as filters

from quizzes.models import VariantGroup


class VariantGroupFilter(django_filters.FilterSet):
    test_type = filters.NumberFilter(field_name="test_type", required=True)

    class Meta:
        model = VariantGroup
        fields = ('test_type',)
