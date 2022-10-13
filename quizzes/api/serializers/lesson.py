from rest_framework import serializers

from base import abstract_serializer
from quizzes.models import Lesson


class LessonSerializer(abstract_serializer.NameSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
            'icon',
        )


class LessonWithTestTypeLessonSerializer(abstract_serializer.NameSerializer):
    test_type_lesson_id = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            # 'id',
            'name',
            'icon',
            'test_type_lesson_id'
        )

    @staticmethod
    def get_test_type_lesson_id(obj):
        return obj.test_type_lessons.all()[0].id
