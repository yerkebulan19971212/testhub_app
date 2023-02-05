from rest_framework import serializers
from quizzes.models import Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = (
            'grade_ball',
            'grade_error',
            'comment'
        )
