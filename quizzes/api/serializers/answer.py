from rest_framework import serializers

from quizzes.models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'id',
            'answer',
            'math'
        )


class AnswerFinishedSerializer(serializers.ModelSerializer):
    is_correct_answered = serializers.BooleanField()

    class Meta:
        model = Answer
        fields = (
            'id',
            'answer',
            'math',
            'is_correct_answered'
        )
