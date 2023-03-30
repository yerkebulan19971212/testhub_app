from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.paginate import SimplePagination
from quizzes.api.serializers import (SaveLessonPairsForUserSerializer,
                                     UserVariantsSerializer,
                                     VariantGroupSerializer, CountrySerializer,
                                     UniversityListSerializer)
from quizzes.filters import CountryFilter, UniversityFilter
from quizzes.models import UserVariant, VariantGroup, Country, University


class CountryListView(generics.ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.filter(is_active=True).annotate(
        university_count=Count(
            'cities__universities',
            filter=Q(cities__universities__is_active=True)
        )
    ).order_by("order")
    pagination_class = SimplePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CountryFilter


country_list = CountryListView.as_view()


class UniversityListView(generics.ListAPIView):
    serializer_class = UniversityListSerializer
    queryset = University.objects.filter(is_active=True).annotate(
        speciality_count=Count(
            'university_specialities',
            filter=Q(university_specialities__speciality__is_active=True)
        )
    ).order_by("order")
    pagination_class = SimplePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = UniversityFilter


university_list = UniversityListView.as_view()
