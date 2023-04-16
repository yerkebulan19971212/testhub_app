from django.db.models import Count, Q, Sum, Avg, DecimalField, IntegerField, \
    Prefetch
from django.db.models.functions import Coalesce, Round
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.paginate import SimplePagination
from quizzes.api.serializers import (SaveLessonPairsForUserSerializer,
                                     UserVariantsSerializer,
                                     VariantGroupSerializer, CountrySerializer,
                                     UniversityListSerializer)
from quizzes.filters.university import SpecialityFilter
from universities.api.serializers.universities import (
    UniversitySpecialityListSerializer,
    UniversitySerializer, SpecialityShowListSerializer
)
from quizzes.filters import CountryFilter, UniversityFilter
from quizzes.models import UserVariant, VariantGroup, Country, University, \
    Speciality, UniversitySpeciality
from universities.models import UniversityDetail


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
    queryset = University.objects.filter(is_active=True).prefetch_related(
        'comfort_university__comfort',
        'university_images'
    ).annotate(
        speciality_count=Count(
            'university_specialities',
            filter=Q(university_specialities__speciality__is_active=True)
        )
    )
    lookup_field = 'pk'

    def get_queryset(self):
        university_details = UniversityDetail.objects.all().order_by('order')
        queryset = self.queryset.prefetch_related(
            Prefetch('university_details', queryset=university_details)
        )
        return queryset


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


kazakhstan_university_list = KazakhstanUniversityListView.as_view()


class UniversitySpecialityListView(generics.ListAPIView):
    serializer_class = UniversitySpecialityListSerializer
    queryset = UniversitySpeciality.objects.filter(speciality__is_active=True)
    pagination_class = SimplePagination
    filter_backends = [DjangoFilterBackend]

university_speciality_list = UniversitySpecialityListView.as_view()


class SpecialityListView(generics.ListAPIView):
    serializer_class = SpecialityShowListSerializer
    queryset = Speciality.objects.filter(is_active=True)
    pagination_class = SimplePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = SpecialityFilter

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            score=Coalesce(Avg('university_specialities__score',
                               output_field=IntegerField()), 0)
        ).annotate(
            grant=Coalesce(Sum('university_specialities__grant'), 0)
        )
        return queryset


speciality_list = SpecialityListView.as_view()


class SpecialityView(generics.RetrieveAPIView):
    serializer_class = SpecialityShowListSerializer
    queryset = Speciality.objects.filter(is_active=True)
    pagination_class = SimplePagination
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            score=Coalesce(Avg('university_specialities__score',
                               output_field=IntegerField()), 0)
        ).annotate(
            grant=Coalesce(Sum('university_specialities__grant'), 0)
        )
        return queryset


speciality = SpecialityView.as_view()
