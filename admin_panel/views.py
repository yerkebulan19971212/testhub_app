from django.db import transaction
from django.shortcuts import render
import io
from quizzes.models import Lesson, TestType, TestTypeLesson, Question


def index(request):
    return render(request, 'admin_panel/index.html')


def add_question(request):
    if request.method == 'POST':
        lesson = request.POST.get('lesson')
        # file = request.FILES['file'].read()
        print("request.body")
        print(request.POST.get('lesson'))
        print(request.POST)
        print(request.FILES)
        print("request.body")
        # buffer = io.BytesIO()
        with request.FILES['file'] as f:
            print(f.read())
            with transaction.atomic():
                line = "s"
                answers = []
                questions_texts = []
                while line:
                    line = f.readline()
                    if not line.strip():
                        print(questions_texts)
                    correct = True
                    question = Question.objects.create(
                        question=questions_texts[0],
                    )

        # file.t
        # with transaction.atomic():
            # topic = self.kwargs['topic']

            # file_name = default_storage.save("txt_file/" + file.name, file)
            answers = []
            # with open("media/" + file_name) as f:
            #     line = "s"
            #     questions_texts = []
            #     count = 0
            #
            #     while line:
            #         line = f.readline()
            #         if not line.strip():
            #             print(questions_texts)
            #
            #             correct = True
            #             question = Question.objects.create(
            #                 question=questions_texts[0],
            #                 topic_id=topic
            #             )
            #             for i in range(1, len(questions_texts)):
            #                 if i > 1:
            #                     correct = False
            #                 answers.append(
            #                     Answer(
            #                         answer=questions_texts[i],
            #                         correct=correct,
            #                         question=question
            #                     )
            #                 )
            #             count += 1
            #             questions_texts = []
            #         else:
            #             text = line.strip().replace('<v>', '').replace('<va>',
            #                                                            '')
            #             if "<q>" in text:
            #                 text = text.replace("<q>", "")[3:].strip()
            #             questions_texts.append(text)
            # Answer.objects.bulk_create(answers)
            # print(count)
        # return Response()
    # if request.method == 'GET':
    test_types_lessons = TestTypeLesson.objects.select_related(
        'lesson', 'test_type'
    ).filter(
        test_type__name_en='ent'
    )
    context = {
        "test_types_lessons": test_types_lessons,
    }
    return render(
        request, 'admin_panel/contents/add_question.html', context=context)
