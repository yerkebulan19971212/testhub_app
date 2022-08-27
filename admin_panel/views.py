from django.shortcuts import render

from quizzes.models import Lesson, TestType


def index(request):
    return render(request, 'admin_panel/index.html')


def add_question(request):
    if request.method == 'GET':
        lessons = Lesson.objects.all()
        test_types = TestType.objects.all()
        context = {
            "lessons": lessons,
            "test_types": test_types
        }
        return render(
            request, 'admin_panel/contents/add_question.html', context=context)
