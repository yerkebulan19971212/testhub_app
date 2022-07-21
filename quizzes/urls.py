from django.urls import path, include

from quizzes.api.api_views import test_type_view, lesson_by_test_type

lesson_urlpatterns = [
    path('by-test-type', lesson_by_test_type, name='lesson_by_test_type')
]

urlpatterns = [
    path('test-type-list/', test_type_view),
    path('lesson/', include(lesson_urlpatterns)),
]
