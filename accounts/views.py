from rest_framework import status
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from coreapi import Field
from .models import EmailOTP, PhoneOTP, User
from .serializer import (AvatarSerializer, ChangePasswordSerializer,
                         EmailOtpSerializer, EmailOTPValidateSerializer,
                         ForgotPasswordSerializer, PhoneOtpSerializer,
                         PhoneOTPValidateSerializer, UserRegistration)


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegistration
    queryset = User.objects.all()


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


# class ClientLoginView(TokenObtainPairView):
#     serializer_class = TokenObtainPairSerializer
#
#     def post(self, request, *args, **kwargs):
#         username = self.request.data.get('username').lower()
#         if "@" in username:
#             user = User.objects.filter(email=username)
#         else:
#             user = User.objects.filter(username=username)
#         if user:
#             user = user.first()
#         else:
#             return Response({"detail": "Такой пользователь не найден"},
#                             status=status.HTTP_400_BAD_REQUEST)
#         company = user.company
#         if company and str(user.role.name) == 'client':
#             if company.confirm is not True:
#                 return Response({"detail": "Ваша заявка еще не принято"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#         role = user.role
#         if role:
#             if str(role.name.lower()) != 'client':
#                 return Response({"detail": "вы не являетесть клиентом"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"detail": "role net"},
#                             status=status.HTTP_400_BAD_REQUEST)
#         return super().post(request, *args, **kwargs)


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