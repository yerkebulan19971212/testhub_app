from rest_framework import serializers

from quizzes.models import University, Country, Speciality, \
    UniversitySpeciality
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


class SpecialityListSerializer(abstract_serializer.NameSerializer):

    class Meta:
        model = Speciality
        fields = (
            'id',
            'icon',
            'name',
            'short_name',
            'name_code',
            'code',
        )


class UniversitySpecialityListSerializer(abstract_serializer.NameSerializer):
    speciality = serializers.SerializerMethodField()

    class Meta:
        model = UniversitySpeciality
        fields = (
            'id',
            'speciality',
            'score',
            'grant'
        )
    def get_speciality(self, obj):
        return SpecialityListSerializer(obj.speciality, context=self.context).data
