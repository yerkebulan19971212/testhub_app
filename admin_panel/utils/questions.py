import random
from typing import List

from django.db.models import Count

from accounts.models import User
from quizzes.models import CommonQuestion, Question, Answer, Variant, \
    UserVariant, AnswerSign, TopicQuestion
from bs4 import BeautifulSoup


def create_question(
        questions_texts, lesson_question_level, variant_group,
                    order=0, topic=None ):
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
    if topic:
        TopicQuestion.objects.get_or_create(
            topic=topic,
            question=test_question
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


def question_lql_list(
        lesson_question_levels,
        variant_ids: List[int],
        unique_percent: int,
        variant_group: int
):
    question_elements = []
    for lql in lesson_question_levels:
        question_list = []
        unique_question_number = lql.number_of_questions * unique_percent // 100
        for v in variant_ids:
            var_questions = Question.objects.filter(
                variant_questions__variant_id=v,
                lesson_question_level=lql
            ).distinct()[:unique_question_number]
            question_list += list(set(list(var_questions)))
        if len(question_list) >= lql.number_of_questions:
            number_of_questions = lql.number_of_questions // 2
        else:
            number_of_questions = lql.number_of_questions
        questions = Question.objects.filter(
            variant_questions__isnull=True,
            variant_group_id=variant_group,
            lesson_question_level=lql
        ).annotate(
            variant_question_count=Count('variant_questions')
        ).order_by('variant_question_count')[:number_of_questions]
        question_list += list(set(list(questions)))
        question_elements += random.sample(
            question_list, lql.number_of_questions)
    return question_elements