from base.abstract_serializer import NameSerializer
from quizzes.models import TestType


class TestTypeSerializer(NameSerializer):
    class Meta:
        model = TestType
        fields = (
            'id',
            'name',
            'icon'
        )
