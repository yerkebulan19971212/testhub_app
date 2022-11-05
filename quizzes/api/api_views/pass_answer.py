from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from quizzes.api.serializers import (FinishByLessonSerializer,
                                     PassAnswerSerializer)
from quizzes.models import PassAnswer, Question, QuizEventQuestion


class PassAnswerByLessonView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PassAnswer.objects.all()
    serializer_class = PassAnswerSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        answers = self.request.data.get('answers')
        question = self.request.data.get('question')
        quiz_event = self.request.data.get('quiz_event')
        try:
            PassAnswer.objects.filter(
                question_id=question,
                user=user,
                quiz_event_id=quiz_event
            ).delete()

            pass_ans = [
                PassAnswer(
                    answer_id=ans,
                    question_id=question,
                    user=user,
                    quiz_event_id=quiz_event)
                for ans in answers]
            PassAnswer.objects.bulk_create(pass_ans)
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_200_OK)


pass_answer_by_lesson_view = PassAnswerByLessonView.as_view()


class FinishByLessonView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FinishByLessonSerializer

    def post(self, request, *args, **kwargs):
        quiz_event = self.request.data.get('quiz_event')
        questions = Question.objects.filter(
            quiz_event_questions__quiz_event_id=quiz_event)
        for q in questions:
            pass_answers = PassAnswer.objects.\
                select_related('question',
                               'question__lesson_question_level',
                               'question__lesson_question_level__question_level',
                               'answer')\
                .filter(question=q, quiz_event_id=quiz_event)
            for p in pass_answers:
                pass


        return Response({}, status=status.HTTP_200_OK)