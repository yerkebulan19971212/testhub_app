from django.db import transaction
from django.db.models import Count, F, Func, Q, Sum, Avg, Max, Exists, \
    OuterRef, Prefetch
from django.db.models.functions import Coalesce, Round
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from base import exceptions
from base.constant import ChoiceType, Status
from base.service import get_multi_score, get_lessons
from quizzes.api.serializers import (StudentAnswersSerializer,
                                     FinishFullTestSerializer,
                                     GetFullTestResultSerializer,
                                     MarkSerializer,
                                     FullTestQuestionSerializer,
                                     FullTestFinishQuestionByLessonSerializer)
from quizzes.filters.question import FullTestQuestionFilter
from quizzes.models import Question, PassAnswer, QuestionScore, UserVariant, \
    TestTypeLesson, TestFullScore, Mark, Answer, Favorite


class PassStudentAnswerView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StudentAnswersSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        question_id = data.get('question')
        user_variant_id = data.get('user_variant')
        answers = data.get('answers')
        score = 0

        question = Question.objects.get(pk=question_id)
        correct_answers = question.answers.filter(correct=True)
        if not answers:
            PassAnswer.objects.filter(
                user=user,
                user_variant_id=user_variant_id,
                question_id=question_id
            ).delete()
        else:
            try:
                with transaction.atomic():
                    PassAnswer.objects.filter(
                        user=user,
                        user_variant_id=user_variant_id,
                        question_id=question_id
                    ).delete()
                    PassAnswer.objects.bulk_create([
                        PassAnswer(
                            user=user,
                            user_variant_id=user_variant_id,
                            question_id=question_id,
                            answer_id=ans
                        ) for ans in answers
                    ])
                    if question.lesson_question_level.question_level.choice == ChoiceType.CHOICE:
                        if correct_answers[0].id == answers[0]:
                            score += 1
                    else:
                        len_correct_answers = correct_answers.count()
                        user_answers = PassAnswer.objects.filter(
                            id__in=answers)
                        len_student_answers = user_answers.count()
                        if len_correct_answers >= len_student_answers:
                            user_answers = list(set(user_answers))
                            correct_answers = list(
                                set([ans for ans in correct_answers]))
                            score += get_multi_score(user_answers,
                                                     correct_answers)
                    QuestionScore.objects.filter(
                        user_variant_id=user_variant_id,
                        question_id=question_id
                    ).delete()
                    QuestionScore.objects.create(
                        user_variant_id=user_variant_id,
                        question_id=question_id,
                        score=score
                    )
            except Exception as e:
                print(e)
                return Response(
                    {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Success"})


pass_answer = PassStudentAnswerView.as_view()


class FinishFullTestView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # serializer_class = StudentAnswersSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_variant_id = self.kwargs.get('user_variant_id')
        try:
            user_variant = UserVariant.objects.select_related(
                'lesson_group',
                'variant__variant_group__test_type'
            ).get(pk=user_variant_id)
        except UserVariant.DoesNotExist as e:
            raise exceptions.DoesNotExist()
        queryset = TestTypeLesson.objects.select_related('lesson').all()
        lessons = get_lessons(user_variant, queryset)
        lessons = lessons.annotate(
            num_question=Coalesce(
                Count('lesson_question_level__questions', filter=Q(
                    lesson_question_level__questions__variant_questions__variant__user_variant__id=user_variant_id
                )), 0),
            pass_answer=Coalesce(
                Count('lesson_question_level__questions__pass_answers',
                      filter=Q(
                          lesson_question_level__questions__variant_questions__variant__user_variant__id=user_variant_id
                      )), 0),
            points=Coalesce(
                Sum('lesson_question_level__question_level__point',
                    filter=Q(
                        lesson_question_level__questions__variant_questions__variant__user_variant__id=user_variant_id
                    )
                    ),
                0)
        ).annotate(
            unattem=F('num_question') - F('pass_answer')
        ).order_by('-main', 'lesson__order')
        user_variant.status = Status.PASSED
        user_variant.save()
        test_full_score = []
        for lesson in lessons:
            user_score = QuestionScore.objects.aggregate(
                user_score=Coalesce(
                    Sum(
                        'score',
                        filter=Q(
                            user_variant=user_variant,
                            question__lesson_question_level__test_type_lesson_id=lesson.id
                        )
                    ),
                    0))
            test_full_score.append(TestFullScore(
                user=user,
                user_variant=user_variant,
                unattem=lesson.unattem,
                user_score=user_score["user_score"],
                number_of_question=lesson.num_question,
                number_of_score=lesson.points,
                test_type_lesson=lesson,
                accuracy=int(
                    round(100 / lesson.points * user_score["user_score"]))
            ))
        TestFullScore.objects.filter(
            user=user,
            user_variant=user_variant
        ).delete()
        TestFullScore.objects.bulk_create(test_full_score)

        return Response({"detail": "Success"})


finish_full_test = FinishFullTestView.as_view()


class GetFullTestResultView(generics.ListAPIView):
    permissions = (permissions.IsAuthenticated,)
    serializer_class = GetFullTestResultSerializer
    queryset = TestFullScore.objects.all()

    def get_queryset(self):
        user = self.request.user
        user_variant_id = self.kwargs.get('user_variant_id')
        queryset = super().get_queryset().filter(
            user=user,
            user_variant_id=user_variant_id
        )
        return queryset

    def get(self, request, *args, **kwargs):
        user = self.request.user
        lesson_score = self.list(request, *args, **kwargs).data
        user_variant_id = self.kwargs.get('user_variant_id')
        # user_variant = UserVariant.objects.get(pk=user_variant_id)
        test_full_score = TestFullScore.objects.all().values(
            'user_variant__variant'
        ).annotate(
            user_score_ball=Coalesce(Sum('user_score'), 0)
        ).aggregate(
            avg_score=Round(Avg('user_score_ball')),
            max_score=Max('user_score_ball')
        )

        number_of_score = 0
        user_score = 0
        for ls in lesson_score:
            number_of_score += ls["number_of_score"]
            user_score += ls["user_score"]
        user_count = UserVariant.objects.all().count()
        user_score_ball = UserVariant.objects.filter().annotate(
            user_score_ball=Coalesce(Sum('test_full_score__user_score'), 0)
        ).order_by('-user_score_ball')
        rating_count = 0
        for u_v in user_score_ball:
            rating_count += 1
            if user_variant_id == u_v.pk:
                break

        data = {
            "rating": {
                "all": user_count,
                "place": rating_count
            },
            "others_info": test_full_score,
            "user_score": user_score,
            "number_of_score": number_of_score,
            "score_by_lessons": lesson_score,
        }
        return Response(data)


get_full_test_result = GetFullTestResultView.as_view()


class MarkQuestions(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MarkSerializer
    queryset = Mark.objects.all()

    def post(self, request, *args, **kwargs):
        question = self.request.data.get('question', None)
        user_variant = self.request.data.get('user_variant', None)
        obj, create_status = self.queryset.get_or_create(
            question_id=question,
            user_variant_id=user_variant,
            user=self.request.user
        )
        if create_status is False:
            obj.is_mark = not obj.is_mark
            obj.save()
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )


create_mark_questions = MarkQuestions.as_view()


class FinishedQuestionsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FullTestFinishQuestionByLessonSerializer
    queryset = Question.objects.select_related(
        'lesson_question_level__question_level'
    ).all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FullTestQuestionFilter

    def get_queryset(self):
        user = self.request.user
        user_variant_id = self.request.data.get('user_variant_id')
        answers = Answer.objects.filter().annotate(
            is_answer_passed=Exists(PassAnswer.objects.filter(
                user=user,
                user_variant_id=user_variant_id,
                answer_id=OuterRef('pk')
            )),
            is_correct_answered=Exists(PassAnswer.objects.filter(
                user=user,
                answer__correct=True,
                user_variant_id=user_variant_id,
                answer_id=OuterRef('pk')
                ))
        )
        queryset = super().get_queryset().prefetch_related(
            Prefetch('answers', queryset=answers)
        ).annotate(
            is_favorite=Exists(
                Favorite.objects.filter(
                    user=user,
                    question_id=OuterRef('pk'),
                    is_favorite=True
                ))
        ).annotate(
            is_correct=Exists(PassAnswer.objects.filter(
                user=user,
                user_variant_id=user_variant_id,
                question_id=OuterRef('pk'),
                answer__correct=True
            )))\
        .annotate(
            is_passed=Exists(PassAnswer.objects.filter(
                user=user,
                user_variant_id=user_variant_id,
                question_id=OuterRef('pk'),
            )))
        return queryset


finish_question_list = FinishedQuestionsList.as_view()
