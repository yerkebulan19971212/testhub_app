from rest_framework import serializers
from quizzes.models import Grade, ComplainQuestion


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = (
            'grade_ball',
            'grade_error',
            'comment'
        )


class ComplainQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplainQuestion
        fields = (
            'question',
            'complain_error',
            'comment'
        )
