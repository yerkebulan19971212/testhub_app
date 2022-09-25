from django.urls import include, path

from quizzes.api.api_views import lesson_list, test_type_view, questions_list
from quizzes.api.api_views import (lesson_list,
                                   lesson_list_with_test_type_lesson_view,
                                   test_type_view, tag_list_view)

lesson_urlpatterns = [
    path('list/', lesson_list, name='lesson_list'),
    path('questions_list/', questions_list, name='questions_list'),
]

question_urlpatterns = [
    path('list/', questions_list),

    path('list/', lesson_list, name='lesson_list'),
    path('test-type-lesson-list/', lesson_list_with_test_type_lesson_view),
]
tag_urlpatterns = [
    path('list/', tag_list_view)
]
urlpatterns = [
    path('test-type-list/', test_type_view),
    path('lesson/', include(lesson_urlpatterns)),
    path('question/', include(question_urlpatterns)),
]
