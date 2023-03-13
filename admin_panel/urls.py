from django.urls import include, path
from .views import index, add_question, generation_variants, variant_list, \
    variant, questions, variant_grouop_list, generation_variant_questions, \
    add_too_app

app_name = 'admin_panel'
urlpatterns = [
    path('index/', index, name='index'),
    path('add-question/', add_question, name='add_question'),
    path('variant-grouop-list/', variant_grouop_list, name='variant_grouop_list'),
    path('variant-list/<int:variant_group_id>', variant_list, name='variant_list'),
    path('variant-list/<int:variant_group_id>', variant_list, name='variant_list'),
    path('variant/<int:id>/', variant, name='variant'),
    path('questions/<int:variant_id>/<int:lesson_id>/', questions, name='questions'),
    path('generation-variant-questions/<int:variant_id>/', generation_variant_questions, name='generation_variant_questions'),
    path('add-too-app/<int:variant_id>/', add_too_app, name='add_too_app'),
    path('generation-variants/',
         generation_variants, name='generation_variants'),
]
