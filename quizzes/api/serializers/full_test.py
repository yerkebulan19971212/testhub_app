from rest_framework import serializers


class StudentAnswersSerializer(serializers.Serializer):
    question = serializers.IntegerField(required=True)
    student_test = serializers.IntegerField(required=True)
    answers = serializers.ListSerializer(
        child=serializers.IntegerField(required=True),
        required=True
    )
