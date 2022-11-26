from rest_framework import serializers

from base.abstract_serializer import NameSerializer
from quizzes.models import UserVariant, Variant, VariantGroup


class VariantGroupSerializer(NameSerializer):
    passed_variants = serializers.IntegerField(default=0)
    count_variants = serializers.IntegerField(default=0)

    class Meta:
        model = VariantGroup
        fields = (
            'id',
            'name',
            'icon',
            'duration',
            'passed_variants',
            'count_variants'
        )


class UserVariantsSerializer(serializers.ModelSerializer):
    variant = serializers.IntegerField(source='variant.variant')
    sum_question = serializers.IntegerField(source='variant.sum_question')
    variant_group = serializers.CharField(
        source='variant.variant_group.name_kz')

    class Meta:
        model = UserVariant
        fields = (
            'id',
            'variant',
            'variant_group',
            'sum_question',
            'status'
        )
