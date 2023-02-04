from django.db import transaction
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import permissions

from base.constant import ChoiceType
from base.service import get_multi_score
from quizzes.api.serializers import (StudentAnswersSerializer,
                                     FinishFullTestSerializer)
from quizzes.models import Question, PassAnswer, QuestionScore


class PassStudentAnswerView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StudentAnswersSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        question_id = data.get('question')
        user_variant_id = data.get('user_variant')
        answers = data.get('answers')
        score = 0

        question = Question.objects.get(pk=question_id)
        correct_answers = question.answers.filter(correct=True)
        if not answers:
            PassAnswer.objects.filter(
                user=user,
                user_variant_id=user_variant_id,
                question_id=question_id
            ).delete()
        else:
            try:
                with transaction.atomic():
                    PassAnswer.objects.filter(
                        user=user,
                        user_variant_id=user_variant_id,
                        question_id=question_id
                    ).delete()
                    PassAnswer.objects.bulk_create([
                        PassAnswer(
                            user=user,
                            user_variant_id=user_variant_id,
                            question_id=question_id,
                            answer_id=ans
                        ) for ans in answers
                    ])
                    if question.lesson_question_level.question_level.choice == ChoiceType.CHOICE:
                        if correct_answers[0].id == answers[0]:
                            score += 1
                    else:
                        len_correct_answers = correct_answers.count()
                        user_answers = PassAnswer.objects.filter(
                            id__in=answers)
                        len_student_answers = user_answers.count()
                        if len_correct_answers >= len_student_answers:
                            user_answers = list(set(user_answers))
                            correct_answers = list(
                                set([ans for ans in correct_answers]))
                            score += get_multi_score(user_answers, correct_answers)
                    QuestionScore.objects.filter(
                        user_variant_id=user_variant_id,
                        question_id=question_id
                    ).delete()
                    QuestionScore.objects.create(
                        user_variant_id=user_variant_id,
                        question_id=question_id,
                        score=score
                    )
            except Exception as e:
                print(e)
                return Response(
                    {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Success"})


pass_answer = PassStudentAnswerView.as_view()


class FinishFullTestView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FinishFullTestSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        user_variant_id = data.get('user_variant')


finish_full_test = FinishFullTestView.as_view()
