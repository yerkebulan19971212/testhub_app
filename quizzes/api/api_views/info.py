from rest_framework import generics
from rest_framework import permissions

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from base.constant import ErrorType
from quizzes.api.serializers import GradeSerializer, \
    ComplainQuestionSerializer, InfoErrorSerializer
from quizzes.filters.info import InfoFilterByGradeType
from quizzes.models import InfoError
from django_filters.rest_framework import DjangoFilterBackend


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
    filter_backends = [DjangoFilterBackend]
    filterset_class = InfoFilterByGradeType


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
    filter_backends = [DjangoFilterBackend]
    filterset_class = InfoFilterByGradeType

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


complain_info_list_view = ComplainInfoErrorListView.as_view()
