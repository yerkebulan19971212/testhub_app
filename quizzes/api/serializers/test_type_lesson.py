from rest_framework import serializers

from quizzes.models import TestTypeLesson


class GetLessonTestTypeLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTypeLesson
        fields = (
            'id',

        )