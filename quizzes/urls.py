from django.urls import path

from quizzes.api.api_views import test_view

urlpatterns = [
    path('test-view/', test_view.TestTypeView.as_view()),
]
