from django.urls import include, path
from .views import index, add_question
app_name = 'admin_panel'
urlpatterns = [
    path('index/', index, name='index'),
    path('add-question/', add_question, name='add_question'),
]
