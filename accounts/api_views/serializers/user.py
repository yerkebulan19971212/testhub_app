from rest_framework import serializers

from accounts.models import Role, User, UserTestType, City
from quizzes.api.serializers import TestTypeOnlyNameSerializer

from .role import RoleSerializer


class UserRegisterSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'role',
            'password',
        )

    def create(self, validated_data):
        validated_data['role'] = Role.objects.get(name="student")
        validated_data['username'] = validated_data.get('email')
        password = validated_data.get('password')
        user = super().create(validated_data)
        user.set_password(password)
        # user.set_unusable_password()
        user.save()
        return user


class UserRegisterByEmailSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'role',
            'password',
        )

    def create(self, validated_data):
        validated_data['role'] = Role.objects.get(name="student")
        validated_data['username'] = validated_data.get('email')
        password = validated_data.get('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class UserRegisterByPhoneSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone',
            'role',
            'password',
        )

    def create(self, validated_data):
        validated_data['role'] = Role.objects.get(name="student")
        password = validated_data.get('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class AddUserTestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTestType
        fields = (
            'id',
            'user',
            'test_type',
        )


class CitySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = (
            'id',
            'name'
        )

    @staticmethod
    def get_name(obj):
        return obj.name_kz


class MeInformationSerializer(serializers.ModelSerializer):
    test_type = TestTypeOnlyNameSerializer()
    city = CitySerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'avatar',
            'first_name',
            'last_name',
            'phone',
            'email',
            'language',
            'test_type',
            'city'
        )


class UserInformationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone',
            'language',
            'test_type',
            'email',
            'avatar',
            'city'
        )
