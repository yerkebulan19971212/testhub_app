import requests
from django.db import transaction

from quizzes.models import Lesson, QuestionLevel, LessonQuestionLevel, \
    CommonQuestion, Question, Answer, AnswerSign


def get_questions():
    answer_signs = list(AnswerSign.objects.all().order_by('order'))
    print(answer_signs)

    try:
        with transaction.atomic():
            lessons = Lesson.objects.filter(
                name_code__isnull=False,
                name_code='informatics').order_by('id')
            print(lessons)
            question_level = QuestionLevel.objects.all().order_by('order')
            for lesson in lessons:
                url = 'http://127.0.0.1:8000/api/v1/quizzes/get-all-question/?lesson_code=' + lesson.name_code
                print(url)
                while url:

                    start_index, end_index = 0, 5
                    r = requests.get(url=url).json()
                    url = r.get('next')
                    result = r.get('results')
                    print(url)
                    for ql in question_level:
                        lesson_question_leve = LessonQuestionLevel.objects.filter(
                            question_level=ql,
                            test_type_lesson__lesson=lesson
                        )
                        print(lesson_question_leve)
                        for rr in result[start_index: end_index]:
                            common_question = rr.get('common_question')
                            print(common_question)
                            c = None
                            math = False
                            if common_question:
                                c, _ = CommonQuestion.objects.get_or_create(
                                    text=common_question.get('text'),
                                    # file=common_question.get('file')
                                )
                            question_text = rr.get('question')
                            if 'math-tex' in question_text or 'img' in question_text:
                                math = True
                            q, _ = Question.objects.get_or_create(
                                common_question=c,
                                lesson_question_level=lesson_question_leve.first(),
                                question=question_text,
                                math=math,
                                variant_group_id=2
                            )
                            answers = rr.get('answer')
                            ans_bulk = []
                            for i, ans in enumerate(answers):
                                a_math = False
                                answer = ans.get('answer')
                                if 'math-tex' in answer or 'img' in answer:
                                    a_math = True
                                ans_bulk.append(
                                    Answer(
                                        question=q,
                                        answer=ans.get('answer'),
                                        correct=ans.get('correct'),
                                        math=a_math,
                                        answer_sign=answer_signs[i]
                                    )
                                )
                            Answer.objects.bulk_create(ans_bulk)
                        start_index += 5
                        end_index += 5
                print('end lesson =========', lesson.id)
            print('add-question')
    except Exception as e:
        print('error catch')
        print(e)