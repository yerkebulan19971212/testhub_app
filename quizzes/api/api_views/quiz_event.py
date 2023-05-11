from django.db import transaction
from django.db.models import Prefetch, Exists, OuterRef, Sum, Count, Q
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from base.constant import QuizzesType
from quizzes.api.serializers import (LessonNameSerializer, QuestionsSerializer,
                                     QuizEventInformationSerializer,
                                     QuizEventSerializer, QuizSerializer,
                                     QuizTestPassAnswerSerializer)
from quizzes.filters import QuestionByLessonFilterByEvent
from quizzes.models import Answer, Question, QuizEvent, QuizEventQuestion, \
    Favorite, PassAnswer, QuestionQuizEventScore


class CreateQuizEventByLessonView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuizEventSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        lesson = self.request.data.get('lesson')
        num_of_question = 15
        try:
            questions = Question.objects.filter(
                lesson_question_level__test_type_lesson_id=lesson
            )[:num_of_question]
            quiz_event = QuizEvent.objects.create(
                quizzes_type=QuizzesType.BY_LESSON,
                test_type_lesson_id=lesson
            )
            QuizEventQuestion.objects.bulk_create([
                QuizEventQuestion(
                    quiz_event=quiz_event,
                    user=user,
                    question=q
                ) for q in questions
            ])
        except Exception as e:
            print(e)
            return Response(
                {"status": False},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "status_code": 0,
                "message": None,
                "result": QuizEventInformationSerializer(quiz_event).data,
                "status": True},
            status=status.HTTP_200_OK)


create_quiz_event_by_lesson_view = CreateQuizEventByLessonView.as_view()


class QuestionsListByLessonView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.select_related(
        "lesson_question_level__question_level"
    ).all()
    serializer_class = QuestionsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionByLessonFilterByEvent

    def get_queryset(self):
        user = self.request.user
        answers = Answer.objects.all()
        return super().get_queryset() \
            .prefetch_related(Prefetch('answers', queryset=answers)) \
            .annotate(
            is_favorite=Exists(
                Favorite.objects.filter(
                    user=user,
                    question_id=OuterRef('pk'),
                    is_favorite=True
                )))

    def get(self, request, *args, **kwargs):
        quiz_event_id = self.request.query_params.get('quiz_event_id')
        try:
            quiz_event = QuizEvent.objects.select_related(
                'test_type_lesson',
                'test_type_lesson__lesson'
            ).get(id=quiz_event_id)
            questions = self.list(request, *args, **kwargs).data
            data = LessonNameSerializer([quiz_event.test_type_lesson.lesson],
                                        many=True).data
            data[0]['questions'] = questions
            user_answers = []
            for q in questions:
                user_answers.append({
                    "question": q.get('id'),
                    "answers": [],
                    "is_mark": False
                })
            data[0]["user_answers"] = user_answers
            result = {"lessons": data}

            return Response({
                "message": "Success",
                "result": result,
                "status_code": 0,
                "status": True
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


questions_list_by_lesson = QuestionsListByLessonView.as_view()


class CreateQuizView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuizEventSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        lesson = self.request.data.get('lesson')

        try:
            quiz_event = QuizEvent.objects.create(
                quizzes_type=QuizzesType.INFINITY_QUIZ,
                test_type_lesson_id=lesson
            )
        except Exception as e:
            print(e)
            return Response(
                {"status": False},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "status_code": 0,
                "message": None,
                "result": QuizSerializer(quiz_event).data,
                "status": True},
            status=status.HTTP_200_OK)


create_quiz = CreateQuizView.as_view()


class QuizQuestionView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.select_related(
        "lesson_question_level__question_level"
    ).all()
    serializer_class = QuestionsSerializer
    lookup_field = None

    def get_object(self):
        user = self.request.user
        quiz_event_id = self.kwargs.get("quiz_event_id")
        quiz_event = QuizEvent.objects.get(pk=quiz_event_id)
        answers = Answer.objects.all()
        question = Question.objects.prefetch_related(
            Prefetch('answers', queryset=answers)
        ).annotate(
            is_favorite=Exists(
                Favorite.objects.filter(
                    user=user,
                    question_id=OuterRef('pk'),
                    is_favorite=True
                )
            )
        ).annotate(
            correct_count=Count('answers', filter=Q(answers__correct=True))
        ).annotate(
            question_count=Count(
                'quiz_event_questions',
                filter=Q(quiz_event_questions__user=user)
            )
        ).filter(
            lesson_question_level__test_type_lesson=quiz_event.test_type_lesson,
            correct_count=1
        ).order_by('question_count')
        question = question.first()
        QuizEventQuestion.objects.create(
            question=question,
            user=user,
            quiz_event=quiz_event
        )
        return question


quiz_question = QuizQuestionView.as_view()


class PassQuizTestAnswerView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuizTestPassAnswerSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        quiz_event_id = data.get('quiz_event_id')
        question_id = data.get('question_id')
        answer_id = data.get('answer_id')

        if answer_id is None:
            try:
                with transaction.atomic():

                    PassAnswer.objects.filter(
                        user=user,
                        quiz_event_id=quiz_event_id,
                        question_id=question_id,
                        answer_id=answer_id
                    ).delete()
                    if answer_id:
                        PassAnswer.objects.create(
                            user=user,
                            quiz_event_id=quiz_event_id,
                            question_id=question_id,
                            answer_id=answer_id
                        )
                        answer = Answer.objects.get(pk=answer_id)
                        if answer.correct:
                            QuestionQuizEventScore.objects.filter(
                                user=user,
                                quiz_event_id=quiz_event_id,
                                question_id=question_id
                            ).delete()
                            QuestionQuizEventScore.objects.create(
                                user=user,
                                quiz_event_id=quiz_event_id,
                                question_id=question_id,
                                score=1
                            )
            except Exception as e:
                print(e)
                return Response(
                    {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Success"})


quiz_test_pass_answer = PassQuizTestAnswerView.as_view()


class CheckQuizTestAnswerView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        question_id = self.kwargs.get('question_id')
        answer = Answer.objects.filter(
            question_id=question_id,
            correct=True
        ).first()
        return Response(
            {
                "result": answer.id
            },
            status=status.HTTP_200_OK
        )


quiz_test_check_answer = CheckQuizTestAnswerView.as_view()


# class FinishQuizTestAnswerView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, *args, **kwargs):
#         quiz_event_id = self.kwargs.get('quiz_event_id')
#         score = QuestionQuizEventScore.objects.filter(
#             quiz_event_id=quiz_event_id
#         ).aggregate(
#             all_score=Coalesce(Sum('score'), 0),
#             all_count=Coalesce(Sum('id'), 0)
#         )
#         pass_answer = PassAnswer.objects.filter(
#             quiz_event_id=quiz_event_id,
#         ).aggregate(
#             correct_answer=Coalesce(Count('answer', filter=Q(answer__correct=True)), 0),
#             all_count=Coalesce(Count('id'), 0)
#         )
#
#         return Response(
#             {
#                 "all_score": score.get("all_score"),
#                 "all_count": pass_answer.get("all_count"),
#                 "correct_answer": pass_answer.get("correct_answer")
#                 # "result": answer.correct
#             },
#             status=status.HTTP_200_OK
#         )

class FinishQuizTestAnswerView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        quiz_event = self.kwargs.get('quiz_event_id')
        quiz_event_obj = QuizEvent.objects.get(pk=quiz_event)
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
            "lesson_id": quiz_event_obj.test_type_lesson_id,
            "lesson_name": quiz_event_obj.test_type_lesson.lesson.name_kz,
        }

        return Response({
            "message": "Success",
            "result": data,
            "status_code": 0,
            "status": True
        }, status=status.HTTP_200_OK)

finish_quiz_test = FinishQuizTestAnswerView.as_view()
