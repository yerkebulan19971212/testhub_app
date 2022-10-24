from rest_framework import serializers

from accounts.models import Role, User, UserTestType

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


class MeInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name'
        )
