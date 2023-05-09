from rest_framework import serializers

from quizzes.api.serializers import LessonNameSerializer, LessonSerializer
from quizzes.models import QuizEvent


class QuizEventSerializer(serializers.Serializer):
    lesson = serializers.IntegerField()


class QuizEventInformationSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(source='test_type_lesson.lesson')
    number_of_question = serializers.IntegerField(default=15)
    test_time = serializers.IntegerField(default=14)

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


class QuizSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(source='test_type_lesson.lesson')

    class Meta:
        model = QuizEvent
        fields = (
            'id',
            'quizzes_type',
            'lesson',
        )

class QuizTestPassAnswerSerializer(serializers.Serializer):
    quiz_event_id = serializers.IntegerField(required=True)
    question_id = serializers.IntegerField(required=True)
    answer_id = serializers.IntegerField()

