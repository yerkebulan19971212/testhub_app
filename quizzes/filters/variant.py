import django_filters
from django_filters import rest_framework as filters

from quizzes.models import VariantGroup, Variant, UserVariant


class VariantGroupFilter(django_filters.FilterSet):
    test_type = filters.NumberFilter(field_name="test_type", required=True)

    class Meta:
        model = VariantGroup
        fields = ('test_type',)


class UserVariantFilter(django_filters.FilterSet):
    variant_group = filters.NumberFilter(
        field_name="variant__variant_group", required=True)

    class Meta:
        model = UserVariant
        fields = (
            'variant_group',
            'status'
        )