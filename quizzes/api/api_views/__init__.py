from .create_flash_cards import create_flash_cards
from .favorites import create_favorite_questions, list_favorites_questions
from .lesson import (lesson_list, lesson_list_variant,
                     test_lesson_list, test_lesson_information_list,
                     lesson_list_with_test_type_lesson_view)
from .list_flash_cards import list_flash_card
from .number_of_questions import list_number_of_questions
from .pass_answer import finish_by_lesson_view, pass_answer_by_lesson_view
from .question import (detail_info_question, questions_list,
                       questions_list_with_only_correct_answer)
from .quiz_event import (create_quiz_event_by_lesson_view,
                         questions_list_by_lesson)
from .tag import tag_list_view
from .test_type import test_type_view
from .test_type_lesson import get_lesson_test_type_lesson_view
from .variants import save_lesson_pairs, user_variants_list, variant_groups
from .full_test import (pass_answer, finish_full_test, get_full_test_result,
                        create_mark_questions)
from .info import (grade_view, complain_question_view, complain_info_list_view,
                   grade_info_list_view)
