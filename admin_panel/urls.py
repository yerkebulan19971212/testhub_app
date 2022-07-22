from django.urls import include, path
from .views import index
app_name = 'admin_panel'
urlpatterns = [
    path('index/', index, name='index'),
]
