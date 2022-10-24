from rest_framework import serializers


class QuizEventSerializer(serializers.Serializer):
    lesson = serializers.IntegerField()
    num_of_question = serializers.IntegerField()
