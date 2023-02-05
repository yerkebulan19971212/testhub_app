from rest_framework import generics
from rest_framework import permissions

from quizzes.api.serializers import GradeSerializer, ComplainQuestionSerializer


class GradeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GradeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


grade_view = GradeCreateView.as_view()


class ComplainQuestionView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ComplainQuestionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


complain_question_view = ComplainQuestionView.as_view()
