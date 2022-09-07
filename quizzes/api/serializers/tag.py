from base import abstract_serializer
from quizzes.models import Tag


class TagListSerializer(abstract_serializer.NameSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name'
        )
