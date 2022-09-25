from rest_framework import serializers
from quizzes.models import FlashCard


class FlashCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields = (
            'id'
            # 'user'
            'question'
            'passed'
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
