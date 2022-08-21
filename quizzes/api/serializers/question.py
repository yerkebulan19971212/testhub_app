from rest_framework import serializers
from quizzes.models import Question


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        field = (
            'id',
            'common_question',
            'lesson_question_level',
            'question',
            'created',
            'modified',
            'order',
            'is_active',
        )
