from rest_framework import serializers

from quizzes.api.serializers.answer import AnswerSerializer
from quizzes.models import Favorite, Question


class QuestionsSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

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
            'answers'
        )


class QuestionDetailSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    is_favorite = serializers.SerializerMethodField()

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
            'answers',
            'is_favorite'
        )

    def get_is_favorite(self, obj):
        try:
            status = (obj.favorites.get(user=self.context['request'].user))
            return status.is_favorite
        except:
            return False
