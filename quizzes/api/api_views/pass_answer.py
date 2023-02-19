from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from base.constant import ChoiceType
from base.service import get_multi_score
from quizzes.api.serializers import (FinishByLessonSerializer,
                                     PassAnswerSerializer)
from quizzes.models import PassAnswer, Question, QuizEventQuestion, \
    QuestionQuizEventScore, Answer


class PassAnswerByLessonView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PassAnswer.objects.all()
    serializer_class = PassAnswerSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_answers = self.request.data.get('user_answers')
        quiz_event = self.kwargs.get('quiz_event')
        pass_ans = []
        quiz_event_score = []
        user_score = 0
        try:
            with transaction.atomic():
                for user_answer in user_answers:
                    answers = user_answer.get('answers')
                    question = user_answer.get('question')
                    for ans in answers:
                        pass_ans.append(PassAnswer(
                            answer_id=ans,
                            question_id=question,
                            user=user,
                            quiz_event_id=quiz_event
                        ))
                    correct_answers = Answer.objects.filter(
                        correct=True,
                        question_id=question
                    )
                    answer_ids = Answer.objects.filter(id__in=answers)
                    score = 0
                    if answer_ids:
                        score = get_multi_score(answer_ids, correct_answers)
                    user_score += score
                    quiz_event_score.append(QuestionQuizEventScore(
                        question_id=question,
                        user=user,
                        quiz_event_id=quiz_event,
                        score=score
                    ))

                PassAnswer.objects.filter(
                    user=user,
                    quiz_event_id=quiz_event
                ).delete()
                PassAnswer.objects.bulk_create(pass_ans)

                QuestionQuizEventScore.objects.filter(
                    quiz_event_id=quiz_event,
                    user=user
                ).delete()
                QuestionQuizEventScore.objects.bulk_create(quiz_event_score)
        except Exception as e:
            print(e)
            return Response({
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "Success",
            "result": None,
            "status_code": 0,
            "status": True
        }, status=status.HTTP_200_OK)


pass_answer_by_lesson_view = PassAnswerByLessonView.as_view()


class FinishByLessonView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        quiz_event = self.kwargs.get('quiz_event')
        questions = Question.objects.select_related(
            "lesson_question_level",
            "lesson_question_level__question_level"
        ).filter(quiz_event_questions__quiz_event_id=quiz_event)
        number_of_score = questions.aggregate(
            number_of_score=Coalesce(
                Sum("lesson_question_level__question_level__point"),
                0
            )
        ).get("number_of_score")
        question_score = QuestionQuizEventScore.objects.filter(
            quiz_event_id=quiz_event
        )
        user_score = question_score.aggregate(
            user_score=Coalesce(Sum('score'), 0)
        ).get("user_score")
        attempt = question_score.values("question").distinct().count()
        question_count = questions.count()
        unattem = question_count - attempt

        data = {
            "user_score": user_score,
            "number_of_score": number_of_score,
            "incorrect_score": number_of_score - user_score,
            "accuracy": int(round(100 / number_of_score * user_score)),
            "attempt": question_count,
            "unattem": unattem,
            "question_number": question_count,
        }

        return Response({
            "message": "Success",
            "result": data,
            "status_code": 0,
            "status": True
        }, status=status.HTTP_200_OK)


finish_by_lesson_view = FinishByLessonView.as_view()
