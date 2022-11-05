from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.constant import QuizzesType
from quizzes.api.serializers import (LessonNameSerializer, QuestionsSerializer,
                                     QuizEventInformationSerializer,
                                     QuizEventSerializer)
from quizzes.filters import QuestionByLessonFilterByEvent
from quizzes.models import Answer, Question, QuizEvent, QuizEventQuestion


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
            {"quiz_event": QuizEventInformationSerializer(quiz_event).data,
             "status": True},
            status=status.HTTP_200_OK)


create_quiz_event_by_lesson_view = CreateQuizEventByLessonView.as_view()


class QuestionsListByLessonView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionByLessonFilterByEvent

    def get_queryset(self):
        answers = Answer.objects.all()
        return super().get_queryset(). \
            prefetch_related(Prefetch('answers', queryset=answers))

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

            return Response({
                "lessons": data,
                "user_answers": []
            })
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


questions_list_by_lesson = QuestionsListByLessonView.as_view()