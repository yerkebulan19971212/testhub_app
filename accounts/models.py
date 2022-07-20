import hashlib
import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.validators import FileExtensionValidator, MinLengthValidator
from django.db import models

from base.abstract_models import TimeStampedModel
from base.service import validate_mb_image, validate_size_image


class Role(TimeStampedModel):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'accounts\".\"role'

    def __str__(self):
        return f"{self.name}"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     **extra_fields):
        """
        Create and save a User with given email, and password.
        """
        if not email:
            raise ValueError('The given username must be set')
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, TimeStampedModel):
    avatar = models.ImageField(
        # upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[validate_size_image, validate_mb_image]
    )
    username = models.CharField(
        max_length=128,
        unique=True
    )
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(
        max_length=11, unique=True, db_index=True, blank=True, null=True)
    role = models.ForeignKey('accounts.Role',
                             related_name='users',
                             on_delete=models.CASCADE,
                             null=True)

    def __str__(self):
        return self.email

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.email = self.email.lower()
        self.username = self.username.lower()
        return super().save()

    def get_full_name(self):
        return " ".join([self.first_name, self.last_name])

    def get_full_name_with_underscore(self):
        return "_".join([self.first_name, self.last_name])

    class Meta:
        db_table = 'accounts\".\"user'


class EmailOTP(TimeStampedModel):
    email = models.EmailField(max_length=128)
    otp = models.CharField(max_length=40, editable=False)
    forgot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    attempts = models.IntegerField(default=0)
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Email OTP Token"
        verbose_name_plural = "Email OTP Tokens"
        db_table = 'accounts\".\"email_otp'

    def __str__(self):
        return "{} - {}".format(self.email, self.otp)

    @classmethod
    def create_otp_for_email(cls, email, forgot=False):
        otp = cls.generate_otp(length=getattr(settings, 'EMAIL_LOGIN_OTP_LENGTH', 6))
        email_otp = EmailOTP.objects.create(email=email,
                                            otp=otp,
                                            forgot=forgot)
        if forgot:
            text = ": " + str(otp) + "\n" + "."
        print(email, otp)
        print(otp, email)
        return email_otp

    @classmethod
    def generate_otp(cls, length=6):
        m = hashlib.sha256()
        m.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
        m.update(os.urandom(16))
        otp = str(int(m.hexdigest(), 16))[-length:]
        return otp


class PhoneOTP(TimeStampedModel):
    phone = models.CharField(max_length=11,
                             unique=True,
                             validators=[
                                 MinLengthValidator(
                                     limit_value=11
                                 )
                             ],
                             blank=True
                             )
    otp = models.CharField(max_length=40, editable=False)
    forgot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    attempts = models.IntegerField(default=0)
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Phone OTP Token"
        verbose_name_plural = "Phone OTP Tokens"
        db_table = 'accounts\".\"phone_otp'

    def __str__(self):
        return "{} - {}".format(self.phone, self.otp)

    @classmethod
    def create_otp_for_phone(cls, phone, forgot=False):
        otp = cls.generate_otp(length=getattr(settings,
                                              'EMAIL_LOGIN_OTP_LENGTH', 6))
        phone_otp = EmailOTP.objects.create(phone=phone,
                                            otp=otp,
                                            forgot=forgot)
        if forgot:
            text = ": " + str(otp) + "\n" + "."
        print(otp, phone)
        return phone_otp

    @classmethod
    def generate_otp(cls, length=6):
        m = hashlib.sha256()
        m.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
        m.update(os.urandom(16))
        otp = str(int(m.hexdigest(), 16))[-length:]
        return otp


class UserTestType(TimeStampedModel):
    user = models.ForeignKey(
        'accounts.User',
        related_name='user_test_type',
        on_delete=models.CASCADE)
    test_type = models.ForeignKey(
        'quizzes.TestType',
        related_name='user_test_type',
        on_delete=models.CASCADE)

    class Meta:
        db_table = 'accounts\".\"user_test_type'
