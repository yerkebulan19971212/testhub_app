from rest_framework import serializers

from quizzes.models import Favorite


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            'id',
            'question',
        )

