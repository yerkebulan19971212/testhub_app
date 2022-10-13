import logging

from django.db import transaction
from django.shortcuts import render
import io
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
                    line = "not None"
                    answers = []
                    answers_bulk_create = []
                    while line:
                        line = f.readline().decode().strip()
                        print('ss', line, 'ss')
                        if not line:
                            if common_question_text:
                                common_question_text = CommonQuestion.objects.get_or_create(
                                    text=common_question_text
                                )
                            print("common_question_text")
                            print(common_question_text)
                            print(question_text)
                            print(lesson_question_level)
                            question = Question.objects.create(
                                lesson_question_level=lesson_question_level,
                                common_question=common_question_text,
                                question=question_text,
                            )
                            answers_correct = [int(i) for i in
                                               answers[-1].split(',')]
                            for i, ans in enumerate(answers[:-1]):
                                if i + 1 in answers_correct:
                                    correct = True
                                else:
                                    correct = False
                                answers_bulk_create.append(Answer(
                                    question=question,
                                    answer=ans,
                                    correct=correct
                                ))
                            print(answers_bulk_create)
                            print("answers_bulk_create")
                            if tag:
                                TagQuestion.objects.create(
                                    question=question,
                                    tag_id=tag
                                )
                            question_text = ''
                            line = 'SSSS'
                            common_question_text = None
                            answers = []
                        else:
                            if 'end' == line[:3]:
                                break
                            if line[0] == '*':
                                common_question_text = line[1:]
                            elif line[0] == '#':
                                question_text = line[1:]
                            else:
                                answers.append(line)
                        print(line)
                        print("line")
                    question_added = True
                    Answer.objects.bulk_create(answers_bulk_create)

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
