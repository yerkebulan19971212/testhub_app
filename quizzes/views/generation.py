from django.db.models import Q, Count, Prefetch
from django.db.models.functions import Coalesce
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from base.paginate import SimplePagination
from quizzes.api.serializers import TestTypeSerializer
from quizzes.models import TestType, VariantGroup, Variant, TestTypeLesson, \
    Question, Answer, CommonQuestion, LessonQuestionLevel, QuestionLevel, Topic
from .generation_serializer import (GenerationTestTypeSerializer,
                                    GenerationVariantGroupSerializer,
                                    GenerationVariantListSerializer,
                                    GenerationGetLessonTestTypeLessonSerializer,
                                    GenerationQuestionByLessonSerializer,
                                    GenerationCommonQuestionSerializer,
                                    GenerationQuestionLevelSerializer,
                                    TopicSerializer)
from ..filters import VariantGroupFilter, TestTypeLessonFilter, TopicFilter
from ..filters.question import GenerateVariantQuestionFilter, \
    GenerateVariantLessonCommonQuestionFilter, GenerateAllQuestionFilter, \
    QuestionLevelFilter
from ..filters.variant import VariantListFilter


class GenerationTestTypeView(generics.ListAPIView):
    queryset = TestType.objects.all()
    serializer_class = GenerationTestTypeSerializer


generation_test_type_view = GenerationTestTypeView.as_view()


class GenerationVariantGroupsView(generics.ListCreateAPIView):
    serializer_class = GenerationVariantGroupSerializer
    queryset = VariantGroup.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = VariantGroupFilter


generation_variant_groups = GenerationVariantGroupsView.as_view()


class VariantsList(generics.ListCreateAPIView):
    serializer_class = GenerationVariantListSerializer
    queryset = Variant.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = VariantListFilter


generation_variant_list = VariantsList.as_view()


class GenerationGetLessonTestTypeLessonsView(generics.ListAPIView):
    queryset = TestTypeLesson.objects.select_related('lesson',
                                                     'test_type').all()
    serializer_class = GenerationGetLessonTestTypeLessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TestTypeLessonFilter

    def get_queryset(self):
        variant_id = self.kwargs.get('variant_id')
        queryset = self.filter_queryset(super().get_queryset()).annotate(
            number_of_questions=Coalesce(
                Count('lesson_question_level__questions',
                      filter=Q(
                          lesson_question_level__questions__variant_questions__variant_id=variant_id)),
                0),
        ).order_by('-main')
        return queryset


generation_get_lesson_test_type_lesson_view = GenerationGetLessonTestTypeLessonsView.as_view()


class GenerationGetQuestionListView(generics.ListAPIView):
    serializer_class = GenerationQuestionByLessonSerializer
    queryset = Question.objects.filter()
    filter_backends = [DjangoFilterBackend]
    filterset_class = GenerateVariantQuestionFilter

    def get_queryset(self):
        answers = Answer.objects.all().order_by('answer_sign__order')
        queryset = super().filter_queryset(
            super().get_queryset()).prefetch_related(
            Prefetch('answers', queryset=answers)
        ).order_by('order')
        return queryset


generation_variant_questions = GenerationGetQuestionListView.as_view()


class GenerationGetQuestionView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GenerationQuestionByLessonSerializer
    queryset = Question.objects.filter()
    lookup_field = 'pk'

    def get_queryset(self):
        answers = Answer.objects.all().order_by('answer_sign__order')
        queryset = super().filter_queryset(
            super().get_queryset()).prefetch_related(
            Prefetch('answers', queryset=answers)
        ).order_by('order')
        return queryset


generation_variant_get_question = GenerationGetQuestionView.as_view()


class GenerationCommonQuestionListView(generics.ListAPIView):
    serializer_class = GenerationCommonQuestionSerializer
    queryset = CommonQuestion.objects.filter()
    filter_backends = [DjangoFilterBackend]
    filterset_class = GenerateVariantLessonCommonQuestionFilter


generation_variant_common_question = GenerationCommonQuestionListView.as_view()


class GenerationCommonQuestionView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GenerationCommonQuestionSerializer
    queryset = CommonQuestion.objects.all()
    lookup_field = 'pk'


generation_common_question = GenerationCommonQuestionView.as_view()


class GenerationCommonQuestionAddView(generics.CreateAPIView):
    serializer_class = GenerationCommonQuestionSerializer
    queryset = CommonQuestion.objects.filter()


generation_add_common_question = GenerationCommonQuestionAddView.as_view()


class GenerationGetAllQuestionListView(generics.ListAPIView):
    serializer_class = GenerationQuestionByLessonSerializer
    queryset = Question.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = GenerateAllQuestionFilter
    pagination_class = SimplePagination

    def get_queryset(self):
        answers = Answer.objects.all().order_by('answer_sign__order')
        queryset = super().filter_queryset(
            super().get_queryset()).prefetch_related(
            Prefetch('answers', queryset=answers)
        ).order_by('-created')
        return queryset


generation_all_questions = GenerationGetAllQuestionListView.as_view()


class GenerationQuestionLevelListView(generics.ListAPIView):
    serializer_class = GenerationQuestionLevelSerializer
    queryset = QuestionLevel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionLevelFilter


generation_all_level = GenerationQuestionLevelListView.as_view()


class TopicListView(generics.ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Topic.objects.select_related('test_type_lesson').all()
    serializer_class = TopicSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TopicFilter


topic_list = TopicListView.as_view()
