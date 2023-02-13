from rest_framework import serializers

from quizzes.models import TestFullScore, Mark


class StudentAnswersSerializer(serializers.Serializer):
    question = serializers.IntegerField(required=True)
    user_variant = serializers.IntegerField(required=True)
    answers = serializers.ListSerializer(
        child=serializers.IntegerField(required=True),
        required=True
    )


class UserAnswersSerializer(serializers.Serializer):
    question = serializers.IntegerField(required=True)
    answers = serializers


class FinishFullTestSerializer(serializers.Serializer):
    user_variant = serializers.IntegerField(required=True)
    user_answers = serializers.ListSerializer(
        child=serializers.IntegerField(required=True),
        required=True
    )


class GetFullTestResultSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source='test_type_lesson.id')
    lesson_name = serializers.CharField(
        source='test_type_lesson.lesson.name_kz')

    class Meta:
        model = TestFullScore
        fields = (
            'lesson_id',
            'lesson_name',
            'unattem',
            'user_score',
            'number_of_question',
            'number_of_score',
            'accuracy'
        )


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = (
            'question',
            'user_variant',
        )
