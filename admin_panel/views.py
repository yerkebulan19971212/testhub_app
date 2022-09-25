from django.shortcuts import render

from quizzes.models import Lesson, TestType, TestTypeLesson


def index(request):
    return render(request, 'admin_panel/index.html')


def add_question(request):
    if request.method == 'GET':
        lessons = Lesson.objects.all()
        test_types = TestType.objects.all()
        test_types_lessons = TestTypeLesson.objects.select_related(
            'lesson', 'test_type'
        ).filter(
            test_type__name_en='ent'
        )
        print(test_types_lessons)
        context = {
            "test_types_lessons": test_types_lessons,
            "lessons": lessons,
            "test_types": test_types
        }
        return render(
            request, 'admin_panel/contents/add_question.html', context=context)
