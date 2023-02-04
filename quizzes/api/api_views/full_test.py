from django.db import transaction
from rest_framework import generics
from rest_framework import permissions

from quizzes.api.serializers import StudentAnswersSerializer
from quizzes.models import Question, PassAnswer


class PassStudentAnswerView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StudentAnswersSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        question_id = data.get('question')
        student_test_id = data.get('student_test')
        answers = data.get('answers')

        question = Question.objects.get(pk=question_id)
        correct_answers = question.answers.filter(correct=True)
        score = 0
        try:
            with transaction.atomic():
                PassAnswer.objects.filter(
                    student_test_id=student_test_id,
                    question_id=question_id
                ).delete()
                PassAnswer.objects.bulk_create([
                    PassAnswer(
                        student_test_id=student_test_id,
                        question_id=question_id,
                        answer_id=ans
                    ) for ans in answers
                ])
                if question.choice_type == AnswerChoiceType.CHOICE:
                    if correct_answers[0].id == answers[0]:
                        score += 1
                else:
                    len_correct_answers = correct_answers.count()
                    user_answers = QuestionAnswer.objects.filter(
                        id__in=answers)
                    len_student_answers = user_answers.count()
                    if len_correct_answers >= len_student_answers:
                        user_answers = list(set(user_answers))
                        correct_answers = list(
                            set([ans for ans in correct_answers]))
                        score += get_multi_score(user_answers, correct_answers)
                QuestionScore.objects.filter(
                    student_test_id=student_test_id,
                    question_id=question_id
                ).delete()
                QuestionScore.objects.create(
                    student_test_id=student_test_id,
                    question_id=question_id,
                    score=score
                )
        except Exception as e:
            print(e)
            return Response({"detail": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Success"})


pass_answer = PassStudentAnswerView.as_view()