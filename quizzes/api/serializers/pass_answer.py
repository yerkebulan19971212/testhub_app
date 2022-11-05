from rest_framework import serializers


class QuestionAnswerSerializer(serializers.Serializer):
    answers = serializers.ListSerializer(
        child=serializers.IntegerField(), required=True)
    question = serializers.IntegerField(required=True)


class PassAnswerSerializer(serializers.Serializer):
    user_answers = serializers.ListSerializer(
        child=QuestionAnswerSerializer(), required=True)


class FinishByLessonSerializer(serializers.Serializer):
    quiz_event = serializers.IntegerField(required=True)
