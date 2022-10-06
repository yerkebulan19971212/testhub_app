from quizzes.models import CommonQuestion


def create_question(questions_texts, variant, lesson):
    if not questions_texts and 'new_line' not in questions_texts:
        return None
    questions_detail = questions_texts.split('new_line')
    question_text = ''
    answer_start = 4
    index_plus = 0
    common_question = None
    if questions_detail[0][0] == "*":
        common_question_text = questions_detail[0][1:].strip()
        common_question_query = CommonQuestion.objects.get_or_create(
            text=common_question_text)
        if common_question_query.exists():
            common_question = common_question_query.first()
        else:
            common_question = CommonQuestion.objects.create(
                text=common_question_text)

        question_text = questions_detail[1][1:].strip()
        index_plus = 1
    elif questions_detail[0][0] == "#":
        answer_start = 3
        question_text = questions_detail[0][1:].strip()

    if 'point' in questions_detail[1 + index_plus]:
        point = int(questions_detail[1 + index_plus].split(' ')[1].strip())
    if 'ch' in questions_detail[2 + index_plus]:
        choice = questions_detail[2 + index_plus].split(' ')[1]
    answers = questions_detail[answer_start:-2]
    correct_answers = list(map(int, questions_detail[-2].split(',')))
    test_question = TestQuestion.objects.create(
        question=question_text,
        text_question=common_question,
        quantity_correct_answers=len(correct_answers),
        choice_type=choice,
        point=point,
        variant_id=variant,
        lesson_id=lesson
    )
    TestQuestionAnswer.objects.bulk_create([
        TestQuestionAnswer(
            test_question=test_question,
            answer=ans.strip(),
            correct=True if (i + 1) in correct_answers else False
        ) for i, ans in enumerate(answers)
    ])
    return test_question
