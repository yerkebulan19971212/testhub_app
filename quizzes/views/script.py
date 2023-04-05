import requests
from django.db import transaction

from quizzes.models import Lesson, QuestionLevel, LessonQuestionLevel, \
    CommonQuestion, Question, Answer, AnswerSign, Variant, VariantQuestion, \
    Topic, TopicQuestion


def get_questions():
    answer_signs = list(AnswerSign.objects.all().order_by('order'))
    print(answer_signs)
    topic = Topic.objects.all().first()

    try:
        with transaction.atomic():
            lessons = Lesson.objects.filter(
                name_code__isnull=False,
                name_code='informatics').order_by('id')
            question_level = QuestionLevel.objects.all().order_by('order')
            variants = Variant.objects.filter(variant_group_id=2)
            variant_q = []
            tpoic_question = []
            for v in variants:

                url = 'http://127.0.0.1:8005/api/v1/quizzes/get-all-question-2/?variant=' + str(v.variant)
                r = requests.get(url=url).json()
                result = r.get('results')
                # print(result)

                for r in result:
                    order_c = 0
                    lesson = Lesson.objects.filter(name_code=r.get("name_code")).first()
                    start_index, end_index = 0, 5
                    for ql in question_level:
                        lesson_question_leve = LessonQuestionLevel.objects.filter(
                            question_level=ql,
                            test_type_lesson__lesson=lesson
                        )
                        for rr in r.get("questions")[start_index: end_index]:
                            common_question = rr.get('common_question')
                            c = None
                            math = False
                            if lesson.math:
                                math = True
                            if common_question:
                                c, _ = CommonQuestion.objects.get_or_create(
                                    text=common_question.get('text').replace(
                                        "<p>", "").replace("</p>", ""),
                                    # file=common_question.get('file')
                                )
                            question_text = rr.get('question')
                            if 'math-tex' in question_text or 'img' in question_text:
                                math = True
                            order_c += 1
                            q, is_created = Question.objects.get_or_create(
                                common_question=c,
                                lesson_question_level=lesson_question_leve.first(),
                                question=question_text.replace("<p>",
                                                               "").replace(
                                    "</p>", ""),
                                math=math,
                                order=order_c,
                                variant_group_id=2
                            )
                            tpoic_question.append(q)
                            variant_q.append(VariantQuestion(
                                variant=v, question=q, order=order_c
                            ))
                            answers = rr.get('answer')

                            ans_bulk = []
                            if is_created:
                                for i, ans in enumerate(answers):
                                    a_math = False
                                    answer = ans.get('answer')
                                    if 'math-tex' in answer or 'img' in answer:
                                        a_math = True
                                    ans_bulk.append(
                                        Answer(
                                            question=q,
                                            answer=ans.get('answer').replace("<p>","").replace(
                                                "</p>", ""),
                                            correct=ans.get('correct'),
                                            math=a_math,
                                            answer_sign=answer_signs[i]
                                        )
                                    )
                            Answer.objects.bulk_create(ans_bulk)
                        start_index += 5
                        end_index += 5
            VariantQuestion.objects.bulk_create(variant_q)
            tpoic_question = list(set(tpoic_question))
            TopicQuestion.objects.bulk_create([
                TopicQuestion(
                    topic=topic,
                    question=q
                ) for q in tpoic_question
            ])
            print('add-question')
    except Exception as e:
        print('error catch')
        print(e)


def change_answer_type():
    Answer.objects.filter(
        answer__icontains='&nbsp'
    ).update(
        math=True
    )
    print('don')

def change_question_type():
    Question.objects.filter(
        question__contains='&nbsp'
    ).update(
        math=True
    )
    print('don')