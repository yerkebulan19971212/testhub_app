from rest_framework import serializers

from quizzes.models import University, Country
from base import abstract_serializer


class CountrySerializer(abstract_serializer.NameSerializer):
    university_count = serializers.IntegerField(default=0)

    class Meta:
        model = Country
        fields = (
            'id',
            'icon',
            'name',
            'university_count',
        )


class UniversityListSerializer(abstract_serializer.NameSerializer):
    speciality_count = serializers.IntegerField(default=0)

    class Meta:
        model = University
        fields = (
            'id',
            'icon',
            'name',
            'short_name',
            'name_code',
            'speciality_count',
        )
