from rest_framework import serializers

from quizzes.models import NumberOfQuestions


class NumberOfQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberOfQuestions
        fields = (
            'id',
            'numbers',
        )
