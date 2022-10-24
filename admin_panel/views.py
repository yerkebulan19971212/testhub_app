import logging

from django.db import transaction
from django.shortcuts import render
import io

from rest_framework import status
from rest_framework.response import Response

from accounts.models import User
from admin_panel.utils.questions import create_question
from quizzes.models import Lesson, TestType, TestTypeLesson, Question, Tag, \
    QuestionLevel, CommonQuestion, Answer, LessonQuestionLevel, TagQuestion, \
    VariantGroup


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
                    variant_group = VariantGroup.objects.get(id=variant_group_id)
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
                                    {"detail": "Что то не так"}, status=status.HTTP_400_BAD_REQUEST)
                            questions_texts = ""
                        else:
                            questions_texts += line.strip() + "new_line"
                        line = f.readline().decode().strip() + ' '
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
    if request.method == 'POST':
        students = User.objects.filter(role__name='student')

