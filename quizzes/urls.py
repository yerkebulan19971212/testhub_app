from django.urls import path

from quizzes.api.api_views import test_type_view

urlpatterns = [
    path('test-type-list/', test_type_view),
]
