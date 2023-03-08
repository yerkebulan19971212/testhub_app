import random

from accounts.models import User
from quizzes.models import CommonQuestion, Question, Answer, Variant, \
    UserVariant, AnswerSign
from bs4 import BeautifulSoup


def create_question(questions_texts, lesson_question_level, variant_group, order):
    if not questions_texts and 'new_line' not in questions_texts:
        return None
    questions_detail = questions_texts.split('new_line')
    question_text = ''
    answer_start = 2
    index_plus = 0
    common_question = None
    if questions_detail[0][0] == "*":
        common_question_text = questions_detail[0][1:].strip()
        common_question_query = CommonQuestion.objects.filter(
            text=BeautifulSoup(common_question_text, "lxml").text)
        if common_question_query.exists():
            common_question = common_question_query.first()
        else:
            common_question = CommonQuestion.objects.create(
                text=common_question_text)

        question_text = questions_detail[1][1:].strip()
        index_plus = 1
    elif questions_detail[0][0] == "#":
        answer_start = 1
        question_text = questions_detail[0][1:].strip()
    math = False
    answer_end = -2
    if questions_detail[-2] == 'math':
        math = True
        answer_end = -3
    answers = questions_detail[answer_start:answer_end]
    correct_answers = list(map(int, questions_detail[answer_end].split(',')))

    test_question = Question.objects.create(
        common_question=common_question,
        lesson_question_level=lesson_question_level,
        question=BeautifulSoup(question_text, "lxml").text,
        math=math,
        variant_group=variant_group,
        order=order
    )

    answer_signs = list(AnswerSign.objects.all().order_by('order'))
    return test_question, [
        Answer(
            question=test_question,
            answer=BeautifulSoup(ans.strip(), "lxml").text,
            correct=True if (i + 1) in correct_answers else False,
            math=math,
            answer_sign=answer_signs[i]
        ) for i, ans in enumerate(answers)
    ]

def user_variant():
    variants = Variant.objects.filter(
        is_active=True, main=True
    )
    variants = list(variants)
    users = User.objects.filter(
        role__name='student'
    )

    user_variants = []
    for u in users:
        random.shuffle(variants, random=random.random)
        for v in variants:
            user_variants.append(UserVariant(
                user=u,
                variant=v
            ))
    UserVariant.objects.bulk_create(user_variants)