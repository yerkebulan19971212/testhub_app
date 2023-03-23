from django.db import transaction
from django.db.models import Q, Count, Prefetch
from django.db.models.functions import Coalesce
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_panel.utils.questions import create_question
from base.paginate import SimplePagination
from quizzes.api.serializers import TestTypeSerializer
from quizzes.models import TestType, VariantGroup, Variant, TestTypeLesson, \
    Question, Answer, CommonQuestion, LessonQuestionLevel, QuestionLevel, \
    Topic, AnswerSign
from .generation_serializer import (GenerationTestTypeSerializer,
                                    GenerationVariantGroupSerializer,
                                    GenerationVariantListSerializer,
                                    GenerationGetLessonTestTypeLessonSerializer,
                                    GenerationQuestionByLessonSerializer,
                                    GenerationCommonQuestionSerializer,
                                    GenerationQuestionLevelSerializer,
                                    TopicSerializer,
                                    GenerationListQuestionByLessonSerializer,
                                    GenerationLessonQuestionLevelSerializer)
from ..filters import VariantGroupFilter, TestTypeLessonFilter, TopicFilter
from ..filters.question import GenerateVariantQuestionFilter, \
    GenerateVariantLessonCommonQuestionFilter, GenerateAllQuestionFilter, \
    QuestionLevelFilter, LessonQuestionLevelFilter
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
    serializer_class = GenerationListQuestionByLessonSerializer
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


class GenerationCreateQuestionView(generics.CreateAPIView):
    serializer_class = GenerationQuestionByLessonSerializer

    def create(self, request, *args, **kwargs):
        answer_signs = list(AnswerSign.objects.all().order_by('order'))
        for i, ans in enumerate(request.data['answers']):
            ans['answer_sign'] = answer_signs[i].id
        return super().create(request, *args, **kwargs)


add_generate_question = GenerationCreateQuestionView.as_view()


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


generation_add_common_question = GenerationCommonQuestionAddView.as_view()


class GenerationGetAllQuestionListView(generics.ListAPIView):
    serializer_class = GenerationListQuestionByLessonSerializer
    queryset = Question.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = GenerateAllQuestionFilter
    pagination_class = SimplePagination

    def get_queryset(self):
        answers = Answer.objects.all().order_by('answer_sign__order')
        queryset = super().filter_queryset(
            super().get_queryset()).prefetch_related(
            Prefetch('answers', queryset=answers)
        ).order_by('-modified', '-common_question__modified')
        return queryset


generation_all_questions = GenerationGetAllQuestionListView.as_view()


class GenerationQuestionLevelListView(generics.ListAPIView):
    serializer_class = GenerationQuestionLevelSerializer
    queryset = QuestionLevel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionLevelFilter


generation_all_level = GenerationQuestionLevelListView.as_view()


class GenerationLessonQuestionLevelListView(generics.ListAPIView):
    serializer_class = GenerationLessonQuestionLevelSerializer
    queryset = LessonQuestionLevel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonQuestionLevelFilter


generation_lesson_level = GenerationLessonQuestionLevelListView.as_view()


class TopicListView(generics.ListCreateAPIView):
    queryset = Topic.objects.select_related('test_type_lesson').all()
    serializer_class = TopicSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TopicFilter


topic_list = TopicListView.as_view()


class ImportQuestionViews(generics.CreateAPIView):
    serializer_class = TopicSerializer

    def post(self, request, *args, **kwargs):
        group_id = request.data.get('group_id')
        level_id = request.data.get('level_id')
        topic_id = request.data.get('topic_id')
        with request.FILES['file'] as f:
            try:
                with transaction.atomic():
                    lesson_question_level = LessonQuestionLevel.objects.get(pk=level_id)
                    variant_group = VariantGroup.objects.get(pk=group_id)
                    topic = Topic.objects.get(pk=topic_id)
                    line = f.readline().decode().strip()
                    questions_texts = ""
                    answers_bulk_create = []
                    while line:
                        if 'end' in line:
                            break
                        if line.strip() == '':
                            question, answers_list = create_question(
                                questions_texts=questions_texts,
                                lesson_question_level=lesson_question_level,
                                variant_group=variant_group,
                                topic=topic
                            )
                            answers_bulk_create += answers_list
                            if question is None:
                                return Response(
                                    {"detail": "Что то не так"},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                            questions_texts = ""
                        else:
                            questions_texts += line.strip() + "new_line"
                        line = f.readline().decode().strip() + ' '
                    Answer.objects.bulk_create(answers_bulk_create)
            except Exception as e:
                print(e)
                message = str(e)
                return Response(
                    {"message": message, "success": False}, status=status.HTTP_200_OK)
        return Response(
            {"success": True}, status=status.HTTP_200_OK)


import_question = ImportQuestionViews.as_view()