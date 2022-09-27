from quizzes.models import NumberOfQuestions
from rest_framework import serializers


class NumberOfQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberOfQuestions
        fields = (
            'id',
            'numbers',
        )
