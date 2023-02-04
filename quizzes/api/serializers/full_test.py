from rest_framework import serializers


class StudentAnswersSerializer(serializers.Serializer):
    question = serializers.IntegerField(required=True)
    user_variant = serializers.IntegerField(required=True)
    answers = serializers.ListSerializer(
        child=serializers.IntegerField(required=True),
        required=True
    )


class FinishFullTestSerializer(serializers.Serializer):
    user_variant = serializers.IntegerField(required=True)
