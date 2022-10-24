from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.constant import QuizzesType
from quizzes.api.serializers import QuizEventSerializer
from quizzes.models import Question, QuizEvent, QuizEventQuestion


class CreateQuizEventByLessonView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuizEventSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        lesson = self.request.data.get('lesson')
        num_of_question = self.request.data.get('num_of_question')
        try:
            questions = Question.objects.filter(
                lesson_question_level__test_type_lesson_id=lesson
            )[:num_of_question]
            quiz_event = QuizEvent.objects.create(
                quizzes_type=QuizzesType.BY_LESSON)
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
            {"quiz_event": quiz_event.id, "status": True},
            status=status.HTTP_200_OK)


create_quiz_event_by_lesson_view = CreateQuizEventByLessonView.as_view()
