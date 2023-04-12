from rest_framework import serializers

from quizzes.models import University, Country, Speciality, \
    UniversitySpeciality, Comfort
from base import abstract_serializer
from universities.models import UniversityImage, Detail, UniversityDetail


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
    short_name = serializers.SerializerMethodField()

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

    def get_short_name(self, obj):
        return obj.short_name_kz


class ComfortSerializer(abstract_serializer.NameSerializer):
    class Meta:
        model = Comfort
        fields = (
            'name',
            'icon',
        )


class UniversityImageSerializer(abstract_serializer.NameSerializer):
    class Meta:
        model = UniversityImage
        fields = (
            'id',
            'image',
        )


class DetailSerializer(abstract_serializer.NameSerializer):
    class Meta:
        model = Detail
        fields = (
            'id',
            'name',
            'name_code',
            'icon',
        )


class UniversityDetailSerializer(serializers.ModelSerializer):
    icon = serializers.FileField(source='detail.icon')
    key = serializers.CharField(source='detail.name_kz')

    class Meta:
        model = UniversityDetail
        fields = (
            'key',
            'value',
            'icon'
        )


class UniversitySerializer(abstract_serializer.NameSerializer):
    speciality_count = serializers.IntegerField(default=0)
    comforts = ComfortSerializer(many=True)
    images = serializers.SerializerMethodField()
    short_name = serializers.SerializerMethodField()
    university_details = UniversityDetailSerializer(many=True)
    description = serializers.SerializerMethodField()

    class Meta:
        model = University
        fields = (
            'id',
            'icon',
            'name',
            'short_name',
            'description',
            'name_code',
            'speciality_count',
            'instagram',
            'telegram',
            'whatsapp',
            'video_link',
            'phone_number',
            'comforts',
            'images',
            'university_details'
        )

    def get_short_name(self, obj):
        return obj.short_name_kz

    def get_description(self, obj):
        return obj.description_kz

    def get_images(self, obj):
        university_images = obj.university_images.all()
        university_images_data = UniversityImageSerializer(university_images, many=True).data
        if university_images_data:
            return [u.get("image") for u in university_images_data]
        return []


class SpecialityListSerializer(abstract_serializer.NameSerializer):
    short_name = serializers.SerializerMethodField()

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

    def get_short_name(self, obj):
        return obj.short_name_kz


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
        return SpecialityListSerializer(obj.speciality,
                                        context=self.context).data

class SpecialityShowListSerializer(abstract_serializer.NameSerializer):
    score = serializers.IntegerField(default=0)
    grant = serializers.IntegerField(default=0)
    short_name = serializers.SerializerMethodField()

    class Meta:
        model = Speciality
        fields = (
            'id',
            'icon',
            'name',
            'short_name',
            'name_code',
            'code',
            'score',
            'grant'
        )

    def get_short_name(self, obj):
        return obj.short_name_kz