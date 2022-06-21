from django.contrib.auth.password_validation import validate_password
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import EmailOTP, Role, User, PhoneOTP


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'id',
            'name_ru',
        )


class UserRegistration(WritableNestedModelSerializer,
                       serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'role',
            'phone',
            'email',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone')
        if User.objects.filter(email=email).exists():
            raise ValidationError("email сущевствует")
        if User.objects.filter(phone=phone).exists():
            raise ValidationError("номер сущевствует")

        return attrs

    def create(self, validated_data):
        validated_data['is_active'] = False
        validated_data['username'] = str(validated_data['username']).lower()
        validated_data['email'] = str(validated_data['email']).lower()
        password = validated_data.get('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user


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