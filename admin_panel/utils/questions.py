from quizzes.models import CommonQuestion, Question, Answer
from bs4 import BeautifulSoup


def create_question(questions_texts, lesson_question_level):
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
    print(question_text)
    correct_answers = list(map(int, questions_detail[answer_end].split(',')))

    test_question = Question.objects.create(
        common_question=common_question,
        lesson_question_level=lesson_question_level,
        question=BeautifulSoup(question_text, "lxml").text,
        math=math
    )
    return test_question, [
        Answer(
            question=test_question,
            answer=BeautifulSoup(ans.strip(), "lxml").text,
            correct=True if (i + 1) in correct_answers else False,
            math=math
        ) for i, ans in enumerate(answers)
    ]
