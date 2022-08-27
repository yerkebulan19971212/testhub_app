from django.urls import include, path

from quizzes.api.api_views import (lesson_list,
                                   lesson_list_with_test_type_lesson_view,
                                   test_type_view)

lesson_urlpatterns = [
    path('list/', lesson_list, name='lesson_list'),
    path('test-type-lesson-list/', lesson_list_with_test_type_lesson_view),
]

urlpatterns = [
    path('test-type-list/', test_type_view),
    path('lesson/', include(lesson_urlpatterns)),
]
