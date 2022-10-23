import logging

from django.db import transaction
from django.shortcuts import render
import io

from rest_framework import status
from rest_framework.response import Response

from admin_panel.utils.questions import create_question
from quizzes.models import Lesson, TestType, TestTypeLesson, Question, Tag, \
    QuestionLevel, CommonQuestion, Answer, LessonQuestionLevel, TagQuestion


def index(request):
    return render(request, 'admin_panel/index.html')


def add_question(request):
    question_added = False
    question_added_try = False
    if request.method == 'POST':
        question_added_try = True
        lesson = request.POST.get('lesson')
        question_level = request.POST.get('question_level')
        tag = request.POST.get('tag')
        lesson_question_level = LessonQuestionLevel.objects.get(
            test_type_lesson_id=lesson,
            question_level_id=question_level
        )
        common_question_text = None
        with request.FILES['file'] as f:
            try:
                with transaction.atomic():
                    line = f.readline().decode().strip()
                    questions_texts = ""
                    answers_bulk_create = []
                    while line:
                        if 'end' in line:
                            break
                        if line.strip() == '':
                            question, answers_list = create_question(
                                questions_texts=questions_texts,
                                lesson_question_level=lesson_question_level
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
                question_added = False

    test_types_lessons = TestTypeLesson.objects.select_related(
        'lesson', 'test_type'
    ).filter(
        test_type__name_en='ent'
    )
    tags = Tag.objects.all()
    question_level = QuestionLevel.objects.all()

    context = {
        "test_types_lessons": test_types_lessons,
        "tags": tags,
        "question_level": question_level,
        "question_added": question_added,
        "question_added_try": question_added_try,
    }
    return render(
        request, 'admin_panel/contents/add_question.html', context=context)
