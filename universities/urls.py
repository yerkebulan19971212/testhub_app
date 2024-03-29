from django.urls import include, path

from universities.api.api_views import (
    kazakhstan_university_list, university_list,
    country_list, speciality_list,
    university_speciality_list, university, speciality)

urlpatterns = [
    path('country-list/', country_list),
    path('university-list/', university_list),
    path('kazakhstan-university-list/', kazakhstan_university_list),
    path('speciality-list/', speciality_list),
    path('speciality/<int:pk>/', speciality),
    path('university/<int:pk>/', university),
]
