from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import EmailOTP, PhoneOTP, Role, User


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'id',
            'name_ru',
        )


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'old_password',
            'password',
            'password2'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Пароли отличаются."
            })

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Старый пароль неверный"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class EmailOtpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=128)
    forgot = serializers.BooleanField(default=False)

    class Meta:
        model = EmailOTP
        fields = ('id', 'email', 'forgot')

    def create(self, validated_data):
        otp = self.Meta.model.create_otp_for_email(**validated_data)

        return otp


class EmailOTPValidateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    otp = serializers.CharField(max_length=10)
    forgot = serializers.BooleanField()

    class Meta:
        model = EmailOTP
        fields = ('id',
                  'otp',
                  'forgot')


class PhoneOtpSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=11)
    forgot = serializers.BooleanField(default=False)

    class Meta:
        model = PhoneOTP
        fields = ('id', 'phone', 'forgot')

    def create(self, validated_data):
        otp = self.Meta.model.create_otp_for_phone(**validated_data)

        return otp


class PhoneOTPValidateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    otp = serializers.CharField(max_length=10)
    forgot = serializers.BooleanField()

    class Meta:
        model = PhoneOTP
        fields = ('id',
                  'otp',
                  'forgot')


class ForgotPasswordSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id',
            'password'
        )

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        instance.save()

        return instance


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'avatar'
        )


class TokenObtainPairSerializerByPhone(TokenObtainPairSerializer):
    username_field = 'phone'


class TokenObtainPairSerializerByEmail(TokenObtainPairSerializer):
    username_field = 'email'
