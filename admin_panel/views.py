from django.db import transaction
from django.shortcuts import render
import io
from quizzes.models import Lesson, TestType, TestTypeLesson, Question, Tag, \
    QuestionLevel, CommonQuestion, Answer, LessonQuestionLevel, TagQuestion


def index(request):
    return render(request, 'admin_panel/index.html')


def add_question(request):
    question_added = False
    if request.method == 'POST':
        lesson = request.POST.get('lesson')
        question_level = request.POST.get('question_level')
        tag = request.POST.get('tag')
        lesson_question_level = LessonQuestionLevel.objects.get(
            test_type_lesson_id=lesson,
            question_level_id=question_level
        )
        common_question_text = None
        with request.FILES['file'] as f:
            with transaction.atomic():
                line = "not None"
                answers = []
                try:
                    while line:
                        line = f.readline().decode().strip()
                        if not line:
                            if not common_question_text:
                                common_question_text = CommonQuestion.objects.get_or_create(
                                    text=common_question_text
                                )
                            question = Question.objects.create(
                                lesson_question_level=lesson_question_level,
                                common_question=common_question_text,
                                question=question_text,
                            )
                            answers_correct = [int(i) for i in
                                               answers[-1].split(',')]
                            answers_bulk_create = []
                            for i, ans in enumerate(answers):
                                if i + 1 in answers_correct:
                                    correct = True
                                else:
                                    correct = False
                                answers_bulk_create.append(Answer(
                                    question=question,
                                    answer=ans,
                                    correct=correct
                                ))
                            Answer.objects.bulk_create(answers_bulk_create)
                            if tag:
                                TagQuestion.objects.create(
                                    question=question,
                                    tag_id=tag
                                )
                            common_question_text = ''
                            question_text = ''
                        else:
                            if line[0] == '*':
                                common_question_text = line[1:]
                            elif line[0] == '#':
                                question_text = line[1:]
                            else:
                                answers.append(line)
                    question_added = True
                except Exception:
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
        "question_added": question_added
    }
    return render(
        request, 'admin_panel/contents/add_question.html', context=context)
