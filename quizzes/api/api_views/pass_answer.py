from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from base.constant import QuizzesType
from quizzes.api.serializers import PassAnswerSerializer
from quizzes.models import PassAnswer


class PassAnswerByLessonView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PassAnswer.objects.all()
    serializer_class = PassAnswerSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        answers = self.request.data.get('answers')
        question = self.request.data.get('question')
        try:
            PassAnswer.objects.filter(
                question_id=question,
                user=user,
                quizzes_type=QuizzesType.BY_LESSON
            ).delete()

            pass_ans = [
                PassAnswer(
                    answer_id=ans,
                    question_id=question,
                    user=user,
                    quizzes_type=QuizzesType.BY_LESSON)
                for ans in answers]
            PassAnswer.objects.bulk_create(pass_ans)
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_200_OK)


pass_answer = PassAnswerByLessonView.as_view()
