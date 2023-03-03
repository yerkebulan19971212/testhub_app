from rest_framework import serializers

from quizzes.api.serializers.answer import AnswerSerializer, \
    AnswerFinishedSerializer
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


class FullTestFinishQuestionSerializer(serializers.ModelSerializer):
    choice = serializers.IntegerField(
        source='lesson_question_level.question_level.choice'
    )
    is_passed = serializers.BooleanField()
    is_correct = serializers.BooleanField()

    class Meta:
        model = Question
        fields = (
            'id',
            'common_question',
            'lesson_question_level',
            'question',
            'choice',
            'math',
            'is_passed',
            'is_correct',
        )


class FullTestFinishQuestionByLessonSerializer(serializers.ModelSerializer):
    answers = AnswerFinishedSerializer(many=True)
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