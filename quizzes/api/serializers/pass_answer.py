from rest_framework import serializers

from quizzes.models import PassAnswer


class PassAnswerSerializer(serializers.Serializer):
    answers = serializers.ListSerializer(child=serializers.IntegerField(),
                                         required=True)
    question = serializers.IntegerField(required=True)
    #
    # def create(self, validated_data):
    #     answers = validated_data.pop('answers')
    #     print(validated_data)
    #     pass_ans = [
    #         PassAnswer(
    #             answer_id=ans,
    #             question=validated_data.get('question'),
    #             user=validated_data.get('user'),
    #             quizzes_type=validated_data.get('quizzes_type'))
    #                 for ans in answers]
    #     print(pass_ans[0].answer_id)
    #     print("pass_ans")
    #     return PassAnswer.objects.bulk_create(pass_ans)
