import math

import requests
from coreapi import Field
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import (CreateAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from base.constant import Status
from quizzes.models import UserVariant, QuestionScore
from .models import EmailOTP, PhoneOTP, User
from .serializer import (AvatarSerializer, ChangePasswordSerializer,
                         EmailOtpSerializer, EmailOTPValidateSerializer,
                         ForgotPasswordSerializer, PhoneOtpSerializer,
                         PhoneOTPValidateSerializer,
                         TokenObtainPairSerializerByEmail,
                         TokenObtainPairSerializerByPhone)


class GoogleJWTView(APIView):
    def post(self, request, *args, **kwargs):
        id_token = request.data.get('id_token', None)
        if not id_token:
            return None

        try:
            # Verify the JWT signature and extract the user ID and email
            response = requests.get(
                f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={id_token}')
            response.raise_for_status()
            user_data = response.json()
        except Exception as e:
            raise AuthenticationFailed('Failed to verify Google id_token')

        # Get or create user
        user, created = User.objects.get_or_create(
            email=user_data['email'])
        if created:
            user.username = user_data['email']
            user.set_unusable_password()
            user.save()

        refresh = TokenObtainPairSerializer.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)


class StaffLoginView(TokenObtainPairView):
    """ логин """
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = self.request.data.get('username').lower()
        if "@" in username:
            user = User.objects.filter(email=username)

        else:
            user = User.objects.filter(username=username)

        if user:
            user = user.first()

        else:
            return Response({"detail": "Такой пользователь не найден"},
                            status=status.HTTP_400_BAD_REQUEST)
        # role = user.role
        # if role:
        #     if str(role.name) == 'client':
        #         return Response({"detail": "вы не являетесть содтрудником"},
        #                         status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({"detail": "role net"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)


class StudentLoginView(TokenObtainPairView):
    """ логин """
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = self.request.data.get('username').lower()
        if "@" in username:
            user = User.objects.filter(email=username)

        else:
            user = User.objects.filter(username=username)

        if user:
            user = user.first()

        else:
            return Response({"detail": "Такой пользователь не найден"},
                            status=status.HTTP_400_BAD_REQUEST)
        # role = user.role
        # if role:
        #     if str(role.name) == 'client':
        #         return Response({"detail": "вы не являетесть содтрудником"},
        #                         status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({"detail": "role net"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)


student_login = StudentLoginView.as_view()


class StudentLoginByPhoneView(TokenObtainPairView):
    """ Login student by phone """
    serializer_class = TokenObtainPairSerializerByPhone


student_login_by_phone = StudentLoginByPhoneView.as_view()


class StudentLoginByEmailView(TokenObtainPairView):
    """ Login student by email """
    serializer_class = TokenObtainPairSerializerByEmail

    def post(self, request, *args, **kwargs):
        request.data['email'] = request.data.get('email').lower()
        return super().post(request, args, kwargs)


student_login_by_email = StudentLoginByEmailView.as_view()


class GenerateEmailOtpView(CreateAPIView):
    serializer_class = EmailOtpSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        if email:
            user = User.objects.filter(email=email)
            if not user.exists():
                return Response({"detail": "такой email не существует"},
                                status=status.HTTP_400_BAD_REQUEST)
            return super().post(request, *args, **kwargs)
        return Response({"detail": "отправили пустою форму"},
                        status=status.HTTP_400_BAD_REQUEST)


class ValidateEmailOTPView(CreateAPIView):
    serializer_class = EmailOTPValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #
        # timestamp_difference = datetime.datetime.now() - datetime.timedelta(
        #     minutes=10
        # )
        try:
            email_otp = EmailOTP.objects.get(
                pk=serializer.data.get('id'),
                used=False,
                forgot=serializer.data.get('forgot', False),
                # timestamp__gte=timestamp_difference
            )

        except EmailOTP.DoesNotExist:
            email_otp = EmailOTP.objects.get(pk=serializer.data.get('id'))
            email_otp.attempts = email_otp.attempts + 1
            email_otp.save()
            return Response({"detail": "ошибочный код "},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.data.get('otp') == email_otp.otp:
            email_otp.used = True
            email_otp.save()
            user = User.objects.filter(
                email=email_otp.email
            ).first()
            user.is_active = True
            user.is_staff = True
            if not serializer.data.get('forgot', False):
                user.user_id = user.pk + 4000
            user.save()
            return Response({
                "detail": "YES",
                "data": {'id': user.id},
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "otp is not correct"},
                            status=status.HTTP_400_BAD_REQUEST)


class GeneratePhoneOtpView(CreateAPIView):
    serializer_class = PhoneOtpSerializer

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone", None)
        if phone:
            user = User.objects.filter(phone=phone)
            if not user.exists():
                return Response({"detail": "такой phone не существует"},
                                status=status.HTTP_400_BAD_REQUEST)
            return super().post(request, *args, **kwargs)
        return Response({"detail": "отправили пустою форму"},
                        status=status.HTTP_400_BAD_REQUEST)


class ValidatePhoneOTPView(CreateAPIView):
    serializer_class = PhoneOTPValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            phone_otp = PhoneOTP.objects.get(
                pk=serializer.data.get('id'),
                used=False,
                forgot=serializer.data.get('forgot', False),
            )

        except PhoneOTP.DoesNotExist:
            phone_otp = PhoneOTP.objects.get(pk=serializer.data.get('id'))
            phone_otp.attempts = phone_otp.attempts + 1
            phone_otp.save()
            return Response({"detail": "ошибочный код "},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.data.get('otp') == phone_otp.otp:
            phone_otp.used = True
            phone_otp.save()
            user = User.objects.filter(
                phone=phone_otp.phone
            ).first()
            user.is_active = True
            user.is_staff = True
            if not serializer.data.get('forgot', False):
                user.user_id = user.pk + 4000
            user.save()
            return Response({
                "detail": "YES",
                "data": {'id': user.id},
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "otp is not correct"},
                            status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(UpdateAPIView):
    serializer_class = ForgotPasswordSerializer
    queryset = User.objects.all()
    lookup_field = None
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        update_response = super().update(request, *args, **kwargs)

        return Response({"detail": "Yes", "data": update_response.data},
                        status=status.HTTP_200_OK)

    def get_object(self):
        pk = self.request.data.get('id')
        query = self.queryset.filter(pk=pk).first()

        return query


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UploadAvatarView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AvatarSerializer
    lookup_field = 'pk'


class GetSchemaView(APIView):
    adss = Field(
        name="param",
        required=True,
        location="query",
        type="string",
        description="A description of the parameter",
    )

    def get(self, request, format=None):
        # your logic here
        return Response(data={'message': 'Success'}, status=status.HTTP_200_OK)


class MyProgresView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        passed_user_variant_count = UserVariant.objects.filter(
            user=user,
            status=Status.PASSED
        ).count()
        score = QuestionScore.objects.filter(
            user_variant__user=user,
            user_variant__status=Status.PASSED,
        ).aggregate(sum_score=Coalesce(Sum('score'), 0)).get('sum_score')
        avg_score = score / passed_user_variant_count if passed_user_variant_count else 0
        max_score = QuestionScore.objects.filter(
            user_variant__user=user
        ).values('user_variant').annotate(
            sum_score=Coalesce(Sum('score'), 0)
        ).order_by('-sum_score')
        if max_score:
            max_score = max_score[0].get('sum_score')
        else:
            max_score = 0

        min_score = QuestionScore.objects.filter(
            user_variant__user=user
        ).values('user_variant').annotate(
            sum_score=Coalesce(Sum('score'), 0)
        ).order_by('sum_score')
        if min_score:
            min_score = min_score[0].get('sum_score')
        else:
            min_score = 0

        return Response({
            "max_score": max_score,
            "min_score": min_score,
            "avg_score": math.ceil(avg_score)
        })


my_progress = MyProgresView.as_view()
