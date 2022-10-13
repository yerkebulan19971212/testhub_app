from rest_framework import serializers

from quizzes.models import Answer


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = (
            'id',
            'answer',
            'correct',
        )
