from django.urls import include, path

from quizzes.api.api_views import (create_favorite_questions,
                                   create_flash_cards,
                                   create_quiz_event_by_lesson_view,
                                   detail_info_question, lesson_list,
                                   lesson_list_with_test_type_lesson_view,
                                   list_favorites_questions, list_flash_card,
                                   pass_answer_by_lesson_view, questions_list,
                                   questions_list_by_lesson,
                                   questions_list_with_only_correct_answer,
                                   tag_list_view, test_type_view,
                                   finish_by_lesson_view, user_variants_list,
                                   variant_groups)
from quizzes.api.api_views.lesson import lesson_list_variant

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
    path('pass-answer-by-lesson/<int:quiz_event>/', pass_answer_by_lesson_view),
    path('finish-by-lesson/<int:quiz_event>/', finish_by_lesson_view),
    # path('create_flash_card/', create_flash_cards),
]

ent_urlpatterns = [
    path('variant-group-list/', variant_groups),
    path('variant-list/', user_variants_list),
    path('lesson-list/', lesson_list_variant)
]
tag_urlpatterns = [
    path('list/', tag_list_view)
]

favorite_urlpatterns = [
    path('', create_favorite_questions),
    path('list/', list_favorites_questions),
]
urlpatterns = [
    path('test-type-list/', test_type_view),
    path('lesson/', include(lesson_urlpatterns)),
    path('question/', include(question_urlpatterns)),
    path('full-test/', include(ent_urlpatterns)),
]
