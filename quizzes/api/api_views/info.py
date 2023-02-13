from rest_framework import generics
from rest_framework import permissions

from base.constant import ErrorType
from quizzes.api.serializers import GradeSerializer, \
    ComplainQuestionSerializer, InfoErrorSerializer
from quizzes.models import InfoError


class GradeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GradeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


grade_view = GradeCreateView.as_view()


class GradeInfoErrorListView(generics.ListAPIView):
    serializer_class = InfoErrorSerializer
    queryset = InfoError.objects.filter(error_type=ErrorType.GRADE,
                                        is_active=True)


grade_info_list_view = GradeInfoErrorListView.as_view()


class ComplainQuestionView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ComplainQuestionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


complain_question_view = ComplainQuestionView.as_view()


class ComplainInfoErrorListView(GradeInfoErrorListView):
    queryset = InfoError.objects.filter(error_type=ErrorType.COMPLAIN,
                                        is_active=True)


complain_info_list_view = ComplainInfoErrorListView.as_view()
