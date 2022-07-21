from rest_framework import serializers

from base import abstract_serializer
from quizzes.models import Lesson


class LessonSerializer(abstract_serializer.NameSerializer):

    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
            'icon'
        )
