from .create_flash_cards import create_flash_cards
from .favorites import create_favorite_questions, list_favorites_questions
from .full_test import (create_mark_questions, finish_full_test,
                        finish_question_list, get_full_test_result,
                        full_pass_answer)
from .info import (complain_info_list_view, complain_question_view,
                   grade_info_list_view, grade_view)
from .lesson import (finished_test_lesson_list, full_test_information,
                     lesson_list, lesson_list_variant,
                     lesson_list_with_test_type_lesson_view,
                     test_lesson_information_list, test_lesson_list)
from .list_flash_cards import list_flash_card
from .number_of_questions import list_number_of_questions
from .pass_answer import finish_by_lesson_view, pass_answer_by_lesson_view
from .question import (detail_info_question, questions_list,
                       questions_list_with_only_correct_answer)
from .quiz_event import (create_quiz, create_quiz_event_by_lesson_view,
                         questions_list_by_lesson, quiz_test_pass_answer,
                         quiz_test_check_answer, finish_quiz_test)
from .tag import tag_list_view
from .test_type import test_type_view
from .test_type_lesson import get_lesson_test_type_lesson_view
from .universities import (country_list, kazakhstan_university_list,
                           university, university_list,
                           university_speciality_list)
from .variants import (save_lesson_pairs, user_variants_list,
                       user_variants_list_count, variant_groups)
