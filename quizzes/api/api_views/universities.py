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
from quizzes.api.serializers.universities import \
    UniversitySpecialityListSerializer, UniversitySerializer
from quizzes.filters import CountryFilter, UniversityFilter
from quizzes.models import UserVariant, VariantGroup, Country, University, \
    Speciality, UniversitySpeciality


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


class UniversityView(generics.RetrieveAPIView):
    serializer_class = UniversitySerializer
    queryset = University.objects.filter(is_active=True).prefetch_related('comfort_university__comfort').annotate(
        speciality_count=Count(
            'university_specialities',
            filter=Q(university_specialities__speciality__is_active=True)
        )
    )
    lookup_field = 'pk'


university = UniversityView.as_view()


class KazakhstanUniversityListView(generics.ListAPIView):
    serializer_class = UniversityListSerializer
    queryset = University.objects.filter(is_active=True).annotate(
        speciality_count=Count(
            'university_specialities',
            filter=Q(university_specialities__speciality__is_active=True)
        )
    ).filter(
        city__country__name_code='kazakhstan_kz'
    ).order_by("order")
    pagination_class = SimplePagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = UniversityFilter


kazakhstan_university_list = KazakhstanUniversityListView.as_view()


class UniversitySpecialityListView(generics.ListAPIView):
    serializer_class = UniversitySpecialityListSerializer
    queryset = UniversitySpeciality.objects.filter(speciality__is_active=True)
    pagination_class = SimplePagination
    filter_backends = [DjangoFilterBackend]


university_speciality_list = UniversitySpecialityListView.as_view()