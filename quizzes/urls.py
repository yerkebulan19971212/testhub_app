from django.urls import include, path

from quizzes.api.api_views import lesson_list, test_type_view

lesson_urlpatterns = [
    path('list/', lesson_list, name='lesson_list')
]

urlpatterns = [
    path('test-type-list/', test_type_view),
    path('lesson/', include(lesson_urlpatterns)),
]
