from django.urls import include, path

from quizzes.api.api_views import (create_favorite_questions,
                                   user_variants_list_count,
                                   create_flash_cards, pass_answer,
                                   create_quiz_event_by_lesson_view,
                                   detail_info_question, finish_by_lesson_view,
                                   lesson_list, test_lesson_information_list,
                                   lesson_list_with_test_type_lesson_view,
                                   list_favorites_questions, list_flash_card,
                                   pass_answer_by_lesson_view, questions_list,
                                   questions_list_by_lesson,
                                   questions_list_with_only_correct_answer,
                                   tag_list_view, test_type_view,
                                   user_variants_list, variant_groups,
                                   save_lesson_pairs, lesson_list_variant,
                                   finish_full_test, get_full_test_result,
                                   test_lesson_list, grade_view,
                                   complain_question_view,
                                   finished_test_lesson_list,
                                   create_mark_questions,
                                   complain_info_list_view,
                                   grade_info_list_view, finish_question_list,
                                   kazakhstan_university_list,
                                   full_test_information, university_list,
                                   country_list,
                                   university_speciality_list, university)
from quizzes.api.api_views.question import full_test_question
from quizzes.views.generation import generation_test_type_view, \
    generation_variant_groups, generation_variant_list, \
    generation_get_lesson_test_type_lesson_view, generation_variant_questions, \
    generation_variant_get_question, generation_variant_common_question, \
    generation_common_question, generation_add_common_question, \
    generation_all_questions, generation_all_level, topic_list, \
    add_generate_question, generation_lesson_level, import_question, \
    generation_question, save_image, generation_update_variant_question, \
    add_generate_question_variant, generation_math_answer, \
    send_questions_to_site

# from quizzes.views.script import create_variant, create_question

lesson_urlpatterns = [
    # path('list/', lesson_list, name='lesson_list'),
]

question_urlpatterns = [
    path('list/', questions_list),
    path('search/', questions_list_with_only_correct_answer),
    path('by-lesson-list/', questions_list_by_lesson),
    path('info/<int:id>/', detail_info_question),

    path('test-type-lesson-list/', lesson_list_with_test_type_lesson_view),
    path('list_flash_card/', list_flash_card),
    path('quize-event-by-lesson/', create_quiz_event_by_lesson_view),
    path('pass-answer-by-lesson/<int:quiz_event>/',
         pass_answer_by_lesson_view),
    path('finish-by-lesson/<int:quiz_event>/', finish_by_lesson_view),
    # path('create_flash_card/', create_flash_cards),
]

ent_urlpatterns = [
    path('variant-group-list/', variant_groups),
    path('variant-list/', user_variants_list),
    path('variant-list-count/', user_variants_list_count),
    path('variant-lesson-list/', lesson_list_variant),
    path('variant-chose-lesson-pairs/<int:pk>/', save_lesson_pairs),
    path('lesson-list/<int:user_variant_id>/', test_lesson_list),
    path('finish-lesson-list/<int:user_variant_id>/',
         finished_test_lesson_list),
    path('lesson-information-list/<int:user_variant_id>/',
         test_lesson_information_list),
    path('get-full-test-result/<int:user_variant_id>/', get_full_test_result),
    path('questions/', full_test_question),
    path('pass_answer/', pass_answer),
    path('finish/<int:user_variant_id>/', finish_full_test),
    path('full-test-information/<int:user_variant_id>/',
         full_test_information),
    path('finish-question/', finish_question_list),
    path('mark/', create_mark_questions)
]

tag_urlpatterns = [
    path('list/', tag_list_view)
]

favorite_urlpatterns = [
    path('', create_favorite_questions),
    path('list/', list_favorites_questions),
]

info_urlpatterns = [
    path('grade/', grade_view),
    path('complain-question_view/', complain_question_view),
    path('grade-info-list/', grade_info_list_view),
    path('complain-info-list/', complain_info_list_view),
]

urlpatterns = [
    path('test-type-list/', test_type_view),
    path('lesson/', include(lesson_urlpatterns)),
    path('question/', include(question_urlpatterns)),
    # path('variant/', create_variant),
    # path('create-questions/', create_question),
]

university_urlpatterns = [
    path('country-list/', country_list),
    path('university-list/', university_list),
    path('kazakhstan-university-list/', kazakhstan_university_list),
    path('speciality-university-list/', university_speciality_list),
    path('university/<int:pk>/', university),
]

generation_url_patterns = [
    path('test-type-list/', generation_test_type_view),
    path('variant-group/', generation_variant_groups),
    path('variant-list/', generation_variant_list),

    path('lesson-list/<int:variant_id>/',
         generation_get_lesson_test_type_lesson_view),
    path('variant-question-list/', generation_variant_questions),
    path('question/<int:pk>/', generation_variant_get_question),
    path('answer/<int:pk>/', generation_math_answer),
    path('common-question-list/', generation_variant_common_question),
    path('common-question/<int:pk>/', generation_common_question),
    path('add-common-question/', generation_add_common_question),
    path('all-question/', generation_all_questions),
    path('add-question/', add_generate_question),
    path('add-question-variant/', add_generate_question_variant),
    path('all-level/', generation_all_level),
    path('all-lesson-level/', generation_lesson_level),
    path('topics/', topic_list),

    path('question-image/', save_image),
    path('update-variant-question/<int:pk>/',
         generation_update_variant_question),
    path('import-question/', import_question),
    path('', generation_question),
    path('send/', send_questions_to_site),
]
