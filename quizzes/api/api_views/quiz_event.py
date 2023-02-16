from django.db.models import Prefetch, Exists, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.constant import QuizzesType
from quizzes.api.serializers import (LessonNameSerializer, QuestionsSerializer,
                                     QuizEventInformationSerializer,
                                     QuizEventSerializer)
from quizzes.filters import QuestionByLessonFilterByEvent
from quizzes.models import Answer, Question, QuizEvent, QuizEventQuestion, \
    Favorite


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
        return super().get_queryset()\
            .prefetch_related(Prefetch('answers', queryset=answers))\
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
