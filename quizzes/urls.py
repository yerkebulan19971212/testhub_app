from django.urls import include, path

from quizzes.api.api_views import lesson_list, test_type_view, questions_list

lesson_urlpatterns = [
    path('list/', lesson_list, name='lesson_list'),
    path('questions_list/', questions_list, name='questions_list'),
]

question_urlpatterns = [
    path('list/', questions_list),

]

urlpatterns = [
    path('test-type-list/', test_type_view),
    path('lesson/', include(lesson_urlpatterns)),
    path('question/', include(question_urlpatterns)),
]
