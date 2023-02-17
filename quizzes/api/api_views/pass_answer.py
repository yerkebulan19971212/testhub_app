from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        score = 0
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
                    score += get_multi_score(answer_ids, correct_answers)
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


class FinishByLessonView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def post(self, request, *args, **kwargs):
        quiz_event = self.kwargs.get('quiz_event')
        questions = Question.objects.select_related(
            "lesson_question_level",
            "lesson_question_level__question_level"
        ).filter(quiz_event_questions__quiz_event_id=quiz_event)
        correct_answer_count = 0
        point = 0
        number_of_score = 0
        user_score = 0
        for q in questions:
            pass_answers = PassAnswer.objects.filter(
                question=q, quiz_event_id=quiz_event
            )
            question_level = q.lesson_question_level.question_level
            number_of_score += question_level.point
            if question_level.choice == ChoiceType.CHOICE:
                pass_answers = pass_answers.filter(answer__correct=True)
                if pass_answers.exists():
                    user_score += 1
            # else:
            #
            # pass_answers = PassAnswer.objects.select_related(
            #     'question',
            #     'question__lesson_question_level',
            #     'question__lesson_question_level__question_level',
            #     'answer')\
            #     .filter()
            # for p in pass_answers:
            #     pass

        data = {
            "user_score": user_score,
            "number_of_score": number_of_score,
            "accuracy": int(round(100 / number_of_score * number_of_score)),
            # "score_by_lessons": lesson_score,
        }
        data = {
            'correct_answer_count': correct_answer_count,
            'answer_count': point
        }
        return Response({
            "message": "Success",
            "result": data,
            "status_code": 0,
            "status": True
        }, status=status.HTTP_200_OK)


finish_by_lesson_view = FinishByLessonView.as_view()
