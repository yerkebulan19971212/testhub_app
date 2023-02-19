from django.db.models import Sum, Q, Count, Prefetch, Exists, Value, \
    BooleanField, OuterRef
from django.db.models.functions import Coalesce, Cast
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base import exceptions
from base.constant import Status
from base.service import get_lessons
from quizzes.api.serializers import (LessonSerializer,
                                     LessonWithTestTypeLessonSerializer,
                                     FullTestLessonSerializer,
                                     FullTestQuestionSerializer)
from quizzes.api.serializers.answer import AnswerSerializer
from quizzes.filters import LessonFilter
from quizzes.models import Lesson, LessonGroup, TestTypeLesson, UserVariant, \
    Question, PassAnswer, Mark, Favorite, Answer


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


lesson_list = LessonListView.as_view()


class LessonListWithTestTypeLessonView(generics.ListAPIView):
    queryset = Lesson.objects.prefetch_related(
        'test_type_lessons',
        'test_type_lessons__test_type'
    ).all()
    serializer_class = LessonWithTestTypeLessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonFilter

    def get_queryset(self):
        language = self.request.headers.get('language', 'kz')
        queryset = super().get_queryset().filter(
            test_type_lessons__language=language)
        return queryset


lesson_list_with_test_type_lesson_view = LessonListWithTestTypeLessonView.as_view()


class LessonListVariantView(generics.ListAPIView):
    queryset = Lesson.objects.prefetch_related(
        'test_type_lessons',
    ).all()
    serializer_class = LessonWithTestTypeLessonSerializer

    def get_queryset(self):
        language = self.request.headers.get('language', 'kz')
        queryset = super().get_queryset().filter(
            test_type_lessons__language=language,
            test_type_lessons__main=False
        )
        return queryset

    def get(self, request, *args, **kwargs):
        data = self.list(request, *args, **kwargs).data
        for lesson in data:
            test_type_lesson_id = lesson.get('test_type_lesson_id')
            lesson_group = LessonGroup.objects \
                .prefetch_related('lesson_pairs') \
                .filter(lesson_pairs__lesson_id=test_type_lesson_id)
            lesson_pair_ids = []
            for lg in lesson_group:
                for lp in lg.lesson_pairs.all():
                    lesson_pair_ids.append(lp.lesson_id)
            if lesson_pair_ids:
                lesson_pair_ids = list(set(lesson_pair_ids))
                lesson_pair_ids.remove(test_type_lesson_id)
            lesson['lesson_pairs'] = lesson_pair_ids
        return Response(data, status=status.HTTP_200_OK)


lesson_list_variant = LessonListVariantView.as_view()


class FullTestLessonList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = TestTypeLesson.objects.select_related('lesson').all()
    serializer_class = FullTestLessonSerializer

    def get_queryset(self):
        user_variant_id = self.kwargs.get('user_variant_id')
        try:
            user_variant = UserVariant.objects.select_related(
                'lesson_group',
                'variant__variant_group__test_type'
            ).get(pk=user_variant_id)
            user_variant.status = Status.CONTINUE
            user_variant.save()
        except UserVariant.DoesNotExist as e:
            raise exceptions.DoesNotExist()

        queryset = super().get_queryset()
        variant = user_variant.variant
        lessons = get_lessons(user_variant, queryset)
        lessons = lessons.annotate(
            number_of_questions=Coalesce(
                Count('lesson_question_level__questions',
                      filter=Q(
                          lesson_question_level__questions__variant_questions__variant=variant)),
                0),
            number_of_score=Coalesce(
                Sum('lesson_question_level__question_level__point',
                    filter=Q(
                        lesson_question_level__questions__variant_questions__variant=variant)),
                0),
            my_score=Coalesce(
                Sum('lesson_question_level__questions__question_score__score',
                    filter=Q(
                        lesson_question_level__questions__question_score__user_variant=user_variant)),
                0),
        ).order_by('-main', 'lesson__order')
        return lessons

    def get(self, request, *args, **kwargs):
        lesson_data = self.list(request, *args, **kwargs).data
        user_variant_id = self.kwargs.get('user_variant_id')
        user = self.request.user

        for lesson in lesson_data:
            lesson_id = lesson["id"]
            pass_answers = PassAnswer.objects.all()
            questions = Question.objects \
                .select_related('lesson_question_level__question_level') \
                .prefetch_related('answers') \
                .prefetch_related(
                Prefetch('pass_answers', queryset=pass_answers)) \
                .filter(
                lesson_question_level__test_type_lesson_id=lesson_id,
                variant_questions__variant__user_variant__id=user_variant_id
            ) \
                .annotate(
                is_mark=Exists(Mark.objects.filter(
                    user=user,
                    user_variant_id=user_variant_id,
                    question_id=OuterRef('pk'),
                    is_mark=True
                ))) \
                .annotate(
                is_favorite=Exists(Favorite.objects.filter(
                    user=user,
                    question_id=OuterRef('pk'),
                    is_favorite=True
                )))

            user_answers = []
            for q in questions:
                answers = [p.answer_id for p in q.pass_answers.all()]
                user_answers.append({
                    "question": q.id,
                    "answers": answers,
                    "is_mark": q.is_mark
                })
            questions_data = FullTestQuestionSerializer(questions, many=True)
            lesson['questions'] = questions_data.data
            lesson['user_answers'] = user_answers

        data = {
            "lessons": lesson_data,
        }
        return Response(data)


test_lesson_list = FullTestLessonList.as_view()


class FullTestLessonInformationList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = TestTypeLesson.objects.select_related('lesson').all()
    serializer_class = FullTestLessonSerializer

    def get_queryset(self):
        user_variant_id = self.kwargs.get('user_variant_id')
        try:
            user_variant = UserVariant.objects.select_related(
                'lesson_group',
                'variant__variant_group__test_type'
            ).get(pk=user_variant_id)
        except UserVariant.DoesNotExist as e:
            raise exceptions.DoesNotExist()

        test_type = user_variant.variant.variant_group.test_type
        variant = user_variant.variant
        queryset = super().get_queryset()
        main_lessons = queryset.filter(main=True, test_type=test_type)
        other_lessons = queryset.filter(
            lesson_pairs__lesson_group=user_variant.lesson_group
        )
        lessons = main_lessons | other_lessons
        lessons = lessons.annotate(
            number_of_questions=Coalesce(
                Count('lesson_question_level__questions',
                      filter=Q(
                          lesson_question_level__questions__variant_questions__variant=variant)),
                0)
        ).order_by('-main', 'lesson__order')
        return lessons


test_lesson_information_list = FullTestLessonInformationList.as_view()


class FullTestFinishedTestLessonList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = TestTypeLesson.objects.select_related('lesson').all()
    serializer_class = FullTestLessonSerializer

    def get_queryset(self):
        user_variant_id = self.kwargs.get('user_variant_id')
        try:
            user_variant = UserVariant.objects.select_related(
                'lesson_group',
                'variant__variant_group__test_type'
            ).get(pk=user_variant_id)
            user_variant.status = Status.CONTINUE
            user_variant.save()
        except UserVariant.DoesNotExist as e:
            raise exceptions.DoesNotExist()

        queryset = super().get_queryset()
        variant = user_variant.variant
        lessons = get_lessons(user_variant, queryset)
        lessons = lessons.annotate(
            number_of_questions=Coalesce(
                Count('lesson_question_level__questions',
                      filter=Q(
                          lesson_question_level__questions__variant_questions__variant=variant)),
                0),
            number_of_score=Coalesce(
                Sum('lesson_question_level__question_level__point',
                    filter=Q(
                        lesson_question_level__questions__variant_questions__variant=variant)),
                0),
            my_score=Coalesce(
                Sum('lesson_question_level__questions__question_score__score',
                    filter=Q(
                        lesson_question_level__questions__question_score__user_variant=user_variant)),
                0),
        ).order_by('-main', 'lesson__order')
        return lessons

    def get(self, request, *args, **kwargs):
        lesson_data = self.list(request, *args, **kwargs).data
        user_variant_id = self.kwargs.get('user_variant_id')
        user = self.request.user

        for lesson in lesson_data:
            lesson_id = lesson["id"]
            pass_answers = PassAnswer.objects.all()
            correct_answers = Answer.objects.filter(
                correct=True,
                question__lesson_question_level__test_type_lesson_id=lesson_id,
                question__variant_questions__variant__user_variant__id=user_variant_id
            )
            questions = Question.objects \
                .select_related('lesson_question_level__question_level') \
                .prefetch_related('answers') \
                .prefetch_related(
                Prefetch('pass_answers', queryset=pass_answers)) \
                .filter(
                lesson_question_level__test_type_lesson_id=lesson_id,
                variant_questions__variant__user_variant__id=user_variant_id
            ) \
                .annotate(
                is_mark=Exists(Mark.objects.filter(
                    user=user,
                    user_variant_id=user_variant_id,
                    question_id=OuterRef('pk'),
                    is_mark=True
                ))) \
                .annotate(
                is_favorite=Exists(Favorite.objects.filter(
                    user=user,
                    question_id=OuterRef('pk'),
                    is_favorite=True
                )))

            user_answers = []
            for q in questions:
                answers = [p.answer_id for p in q.pass_answers.all()]
                user_answers.append({
                    "question": q.id,
                    "answers": answers,
                    "is_mark": q.is_mark
                })
            questions_data = FullTestQuestionSerializer(questions, many=True)
            correct_answers_l = AnswerSerializer(correct_answers, many=True)
            lesson['correct_answer'] = correct_answers_l
            lesson['questions'] = questions_data.data
            lesson['user_answers'] = user_answers
        data = {"lessons": lesson_data}
        return Response(data)


finished_test_lesson_list = FullTestLessonList.as_view()
