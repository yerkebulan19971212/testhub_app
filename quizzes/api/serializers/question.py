from rest_framework import serializers

from quizzes.api.serializers.answer import AnswerSerializer
from quizzes.models import Favorite, Question


class QuestionsSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    choice = serializers.IntegerField(
        source='lesson_question_level.question_level.choice'
    )
    is_favorite = serializers.BooleanField(default=False)

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
            'choice',
            'math',
            'is_favorite',
            'answers',
        )


class QuestionDetailSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    is_favorite = serializers.BooleanField()

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
            'is_favorite',
            'math',
            'answers',
        )


class FullTestQuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    choice = serializers.IntegerField(
        source='lesson_question_level.question_level.choice'
    )
    is_favorite = serializers.BooleanField()

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
            'choice',
            'math',
            'is_favorite',
            'answers'
        )
