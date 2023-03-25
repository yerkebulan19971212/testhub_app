import logging

import requests
from django.db import transaction
from django.db.models import Count, Q, Prefetch
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
import io

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from accounts.models import User
from admin_panel.utils.questions import create_question
from base.constant import TestLang
from quizzes.models import Lesson, TestType, TestTypeLesson, Question, Tag, \
    QuestionLevel, CommonQuestion, Answer, LessonQuestionLevel, TagQuestion, \
    VariantGroup, Variant, VariantQuestion


def variant_grouop_list(request):
    variant_groups = VariantGroup.objects.all()
    context = {
        "variant_groups": variant_groups
    }
    return render(request, 'admin_panel/variant_group.html', context=context)


def create_variant(request, variant_group_id):
    variant_groups = VariantGroup.objects.all()
    context = {
        "variant_groups": variant_groups
    }
    return render(request, 'admin_panel/variants_list.html', context=context)


def variant_list(request, variant_group_id):
    variants = Variant.objects.filter(
        variant_group_id=variant_group_id).order_by('order')
    context = {
        "variants": variants
    }
    return render(request, 'admin_panel/variants_list.html', context=context)


def variant(request, id):
    variant = Variant.objects.get(pk=id)
    variants = Variant.objects.all()
    test_type = variant.variant_group.test_type
    lessons = TestTypeLesson.objects.filter(
        test_type=test_type
    ).annotate(
        number_of_questions=Coalesce(
            Count('lesson_question_level__questions',
                  filter=Q(
                      lesson_question_level__questions__variant_questions__variant=variant)),
            0),
    ).order_by('-main')
    context = {
        "variants": variants,
        "lessons": lessons,
        "variant": variant
    }
    return render(request, 'admin_panel/variant.html', context=context)


def questions(request, variant_id, lesson_id):
    variant = Variant.objects.get(pk=variant_id)
    variants = Variant.objects.all()
    lesson = TestTypeLesson.objects.annotate(
        number_of_questions=Coalesce(
            Count('lesson_question_level__questions',
                  filter=Q(
                      lesson_question_level__questions__variant_questions__variant=variant)),
            0)).get(pk=lesson_id)
    if request.method == 'POST':
        question_added_try = True
        common_question_text = None
        with request.FILES['file'] as f:
            try:
                with transaction.atomic():
                    line = f.readline().decode().strip()
                    questions_texts = ""
                    answers_bulk_create = []
                    variant_question = []
                    variant_group = variant.variant_group
                    lesson_question_levels = LessonQuestionLevel.objects.filter(
                        test_type_lesson_id=lesson_id,
                    )
                    count_q = 0
                    for ll in lesson_question_levels:
                        while line:
                            if 'end_test_q' in line:
                                break
                            if line.strip() == '':
                                count_q += 1
                                question, answers_list = create_question(
                                    questions_texts=questions_texts,
                                    lesson_question_level=ll,
                                    variant_group=variant_group,
                                    order=count_q
                                )
                                answers_bulk_create += answers_list
                                if count_q == 5:
                                    break
                                variant_question.append(VariantQuestion(
                                    question=question,
                                    variant=variant,
                                ))
                                if question is None:
                                    return Response(
                                        {"detail": "Что то не так"},
                                        status=status.HTTP_400_BAD_REQUEST)
                                questions_texts = ""
                            else:
                                questions_texts += line.strip() + "new_line"
                            line = f.readline().decode().strip() + ' '
                        if 'end_test_q' in line:
                            Answer.objects.bulk_create(answers_bulk_create)
                            VariantQuestion.objects.bulk_create(
                                variant_question)
                            break
                question_added = True
            except Exception as e:
                print(e)
                message = str(e)
                question_added = False

    answers = Answer.objects.all().order_by('answer_sign__order')

    questions = Question.objects.filter(
        lesson_question_level__test_type_lesson_id=lesson_id,
        variant_questions__variant_id=variant_id
    ).prefetch_related(
        Prefetch('answers', queryset=answers)
    ).order_by('order')
    context = {
        "questions": questions,
        "variants": variants,
        "lesson": lesson,
        "variant": variant
    }
    return render(request, 'admin_panel/questions.html', context=context)


def index(request):
    return render(request, 'admin_panel/index.html')


def add_question(request):
    question_added = False
    question_added_try = False
    message = ''
    if request.method == 'POST':
        question_added_try = True
        lesson = request.POST.get('lesson')
        question_level = request.POST.get('question_level')
        tag = request.POST.get('tag')
        variant_group_id = request.POST.get('variant_group')

        common_question_text = None
        with request.FILES['file'] as f:
            try:
                with transaction.atomic():
                    lesson_question_level = LessonQuestionLevel.objects.get(
                        test_type_lesson_id=lesson,
                        question_level_id=question_level
                    )
                    variant_group = VariantGroup.objects.get(
                        id=variant_group_id)
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
                                variant_group=variant_group
                            )
                            answers_bulk_create += answers_list
                            if question is None:
                                return Response(
                                    {"detail": "Что то не так"},
                                    status=status.HTTP_400_BAD_REQUEST)
                            questions_texts = ""
                        else:
                            questions_texts += line.strip() + "new_line"
                        line = f.readline().decode().strip() + ' '
                        print(line)
                        print("line")
                    Answer.objects.bulk_create(answers_bulk_create)
                question_added = True
            except Exception as e:
                print(e)
                message = str(e)
                question_added = False

    test_types_lessons = TestTypeLesson.objects.select_related(
        'lesson', 'test_type'
    ).filter(
        test_type__name_en='ent'
    )
    tags = Tag.objects.all()
    question_level = QuestionLevel.objects.all()
    variant_groups = VariantGroup.objects.filter(is_active=True)

    context = {
        "test_types_lessons": test_types_lessons,
        "tags": tags,
        "question_level": question_level,
        "question_added": question_added,
        "question_added_try": question_added_try,
        "variant_groups": variant_groups,
        "message_er": message,
    }
    return render(
        request, 'admin_panel/contents/add_question.html', context=context)


def generation_variants(request):
    context = {}
    if request.method == 'POST':
        variant_group = request.POST.get('variant_group')
        variant_question = []
        # students = User.objects.filter(role__name='student')
        variants = Variant.objects.filter(
            variant_questions__isnull=True,
            variant_group_id=variant_group
        )
        if not variants:
            context['created'] = False
        else:
            context['created'] = False
        test_type_lessons = TestTypeLesson.objects.filter(
            test_type__name_code='ent',
            language=TestLang.KAZAKH
        )
        try:
            with transaction.atomic():
                for tt in test_type_lessons:
                    lesson_question_levels = LessonQuestionLevel \
                        .objects \
                        .select_related('question_level') \
                        .filter(test_type_lesson=tt)
                    print(tt.questions_number)
                    print(tt.lesson.name_kz)
                    print("tt.lesson.name_kz")

                    for lql in lesson_question_levels[
                               :tt.questions_number // 5 + 1]:
                        for v in variants:
                            questions = Question.objects.filter(
                                variant_questions__isnull=True,
                                variant_group_id=variant_group,
                                lesson_question_level=lql
                            )
                            if questions.count() >= lql.number_of_questions:
                                questions = questions[:lql.number_of_questions]
                            if questions:
                                variant_question += [
                                    VariantQuestion(
                                        question=q,
                                        variant=v
                                    ) for q in questions]

                VariantQuestion.objects.bulk_create(variant_question)
        except Exception as e:
            print(e)
    variant_groups = VariantGroup.objects.filter(is_active=True)
    context['variant_groups'] = variant_groups
    return render(
        request, 'admin_panel/contents/variant_create.html', context=context)


def generation_variant_questions(request, variant_id):
    context = {}
    if request.method == 'POST':
        variant = Variant.objects.get(pk=variant_id)
        test_type = variant.variant_group.test_type
        variant_group = variant.variant_group
        test_type_lessons = TestTypeLesson.objects.filter(
            test_type=test_type,
            language=TestLang.KAZAKH
        )

        variant_question = []
        try:
            with transaction.atomic():
                for tt in test_type_lessons:
                    lesson_question_levels = LessonQuestionLevel \
                        .objects \
                        .select_related('question_level') \
                        .filter(test_type_lesson=tt)

                    for lql in lesson_question_levels[
                               :tt.questions_number // 5 + 1]:
                        questions = Question.objects.filter(
                            variant_questions__isnull=True,
                            variant_group=variant_group,
                            lesson_question_level=lql)
                        if questions.count() >= lql.number_of_questions:
                            questions = questions[:lql.number_of_questions]
                        if questions:
                            variant_question += [
                                VariantQuestion(
                                    question=q,
                                    variant=variant
                                ) for q in questions]
                VariantQuestion.objects.bulk_create(variant_question)
        except Exception as e:
            print(e)
        return redirect(
            reverse('admin_panel:variant', kwargs={'id': variant.pk}))

    variant_groups = VariantGroup.objects.filter(is_active=True)
    context['variant_groups'] = variant_groups
    return render(
        request, 'admin_panel/contents/variant_create.html', context=context)


def add_too_app(request, variant_id):
    context = {}
    if request.method == 'POST':
        variant = Variant.objects.get(pk=variant_id)
        test_type = variant.variant_group.test_type
        data = {
            "variant": variant.pk,
            "variant_group": variant.variant_group.pk,
            "is_active": False,
            "sum_question": variant.sum_question,
        }
        print(data)
        print(type(data))
        print("++++++++++++++++++++++++===")
        url = 'http://127.0.0.1:8003/api/v1/quizes/variant/'
        res = requests.post(url=url, json=data)
        print(res)
        print(res.json())
        if res.status_code == 200:
            res_data = res.json()
            print(res_data)
            print("res_data")
            res_status = res_data.get('status')
            if res_status:
                test_type_lessons = TestTypeLesson.objects.filter(
                    test_type=test_type,
                    language=TestLang.KAZAKH
                ).values()
                for tt in test_type_lessons:
                    questions = Question.objects.filter(
                        lesson_question_level__test_type_lesson=tt,
                        variant_questions__variant=variant
                    ).values()
                    for q in questions:
                        answers = Answer.objects.filter(question_id=q.get('id')).values()
                        q['answers'] = answers
                    tt['questions'] = questions
                url_2 = 'http://127.0.0.1:8003/api/v1/quizes/create-questions/'
                print(test_type_lessons)
                print("test_type_lessons")
                # res_2 = requests.post(url=url_2, json=test_type_lessons)
                # print(res_2.json())


        # variant_group = variant.variant_group
        # test_type_lessons = TestTypeLesson.objects.filter(
        #     test_type=test_type,
        #     language=TestLang.KAZAKH
        # )
        #
        # variant_question = []
        # try:
        #     with transaction.atomic():
        #         for tt in test_type_lessons:
        #             lesson_question_levels = LessonQuestionLevel \
        #                 .objects \
        #                 .select_related('question_level') \
        #                 .filter(test_type_lesson=tt)
        #
        #             for lql in lesson_question_levels[
        #                        :tt.questions_number // 5 + 1]:
        #                 questions = Question.objects.filter(
        #                     variant_questions__isnull=True,
        #                     variant_group=variant_group,
        #                     lesson_question_level=lql)
        #                 if questions.count() >= lql.number_of_questions:
        #                     questions = questions[:lql.number_of_questions]
        #                 if questions:
        #                     variant_question += [
        #                         VariantQuestion(
        #                             question=q,
        #                             variant=variant
        #                         ) for q in questions]
        #         VariantQuestion.objects.bulk_create(variant_question)
        # except Exception as e:
        #     print(e)
        return redirect(
            reverse('admin_panel:variant', kwargs={'id': variant.pk}))
