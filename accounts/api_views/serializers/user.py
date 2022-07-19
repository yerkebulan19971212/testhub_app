from accounts import models
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'password',
        )

    def create(self, validated_data):
        validated_data['username'] = validated_data.get('email')
        password = validated_data.get('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class AddUserTestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserTestType
        fields = (
            'id',
            'user',
            'test_type',
        )
