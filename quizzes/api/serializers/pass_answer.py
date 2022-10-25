from rest_framework import serializers


class PassAnswerSerializer(serializers.Serializer):
    answers = serializers.ListSerializer(child=serializers.IntegerField(),
                                         required=True)
    question = serializers.IntegerField(required=True)
    quiz_event = serializers.IntegerField(required=True)


class FinishByLessonSerializer(serializers.Serializer):
    quiz_event = serializers.IntegerField(required=True)
