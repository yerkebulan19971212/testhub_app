from rest_framework import serializers

from quizzes.models import test_type


class TestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = test_type.TestType
        fields = [
            'id',
            'name_kz',
            'name_ru',
            'name_en',
            'order'
        ]
