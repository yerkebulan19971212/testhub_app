from .create_flash_cards import create_flash_cards
from .favorites import create_favorite_questions, list_favorites_questions
from .lesson import lesson_list, lesson_list_with_test_type_lesson_view
from .list_flash_cards import list_flash_card
from .number_of_questions import list_number_of_questions
from .question import (detail_info_question, questions_list,
                       questions_list_by_lesson,
                       questions_list_with_only_correct_answer)
from .tag import tag_list_view
from .test_type import test_type_view
from .test_type_lesson import get_lesson_test_type_lesson_view
from .pass_answer import pass_answer_by_lesson_view
from .quiz_event import create_quiz_event_by_lesson_view
