from quizzes.models import test_type
from rest_framework import serializers


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
