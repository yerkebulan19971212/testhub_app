from django.shortcuts import render


def index(request):
    return render(request, 'admin_panel/index.html')


def add_question(request):
    return render(request, 'admin_panel/contents/add_question.html')