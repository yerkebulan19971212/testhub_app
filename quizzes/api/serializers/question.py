from rest_framework import serializers

from quizzes.api.serializers.answer import AnswerSerializer
from quizzes.models import Question


class QuestionsSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'common_question',
            'lesson_question_level',
            'question',
            'created',
            'modified',
            'order',
            'is_active',
            'answers'
        )
