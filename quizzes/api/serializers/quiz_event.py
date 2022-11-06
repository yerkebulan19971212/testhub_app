from rest_framework import serializers

from quizzes.api.serializers import LessonNameSerializer
from quizzes.models import QuizEvent


class QuizEventSerializer(serializers.Serializer):
    lesson = serializers.IntegerField()


class QuizEventInformationSerializer(serializers.ModelSerializer):
    lesson = LessonNameSerializer(source='test_type_lesson.lesson')
    number_of_question = serializers.IntegerField(default=15)
    test_time = serializers.IntegerField(default=0)

    class Meta:
        model = QuizEvent
        fields = (
            'id',
            'quizzes_type',
            'lesson',
            'number_of_question',
            'status',
            'test_time'
        )

    @staticmethod
    def get_test_time():
        return 14
