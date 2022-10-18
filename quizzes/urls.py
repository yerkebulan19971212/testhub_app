from django.urls import include, path

from quizzes.api.api_views import (create_favorite_questions,
                                   create_flash_cards, detail_info_question,
                                   lesson_list,
                                   lesson_list_with_test_type_lesson_view,
                                   list_favorites_questions, list_flash_card,
                                   questions_list,
                                   questions_list_with_only_correct_answer,
                                   tag_list_view, test_type_view)

lesson_urlpatterns = [
    # path('list/', lesson_list, name='lesson_list'),
]

question_urlpatterns = [
    path('list/', questions_list),
    path('search/', questions_list_with_only_correct_answer),
    path('info/<int:id>/', detail_info_question),

    path('test-type-lesson-list/', lesson_list_with_test_type_lesson_view),
    path('list_flash_card/', list_flash_card),
    # path('create_flash_card/', create_flash_cards),
]
tag_urlpatterns = [
    path('list/', tag_list_view)
]

favorite_urlpatterns = [
    path('create/', create_favorite_questions),
    path('list/', list_favorites_questions),
]
urlpatterns = [
    path('test-type-list/', test_type_view),
    path('lesson/', include(lesson_urlpatterns)),
    path('favorite/', include(favorite_urlpatterns)),
    path('question/', include(question_urlpatterns)),
]
