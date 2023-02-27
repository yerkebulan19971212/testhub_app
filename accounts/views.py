import requests
from rest_framework import status
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from coreapi import Field
from .models import EmailOTP, PhoneOTP, User
from .serializer import (AvatarSerializer, ChangePasswordSerializer,
                         EmailOtpSerializer, EmailOTPValidateSerializer,
                         ForgotPasswordSerializer, PhoneOtpSerializer,
                         PhoneOTPValidateSerializer, UserRegistration)

# from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class GoogleAuthentication(BaseAuthentication):
    def authenticate(self, request):
        id_token = request.META.get('HTTP_AUTHORIZATION', None)
        if not id_token:
            return None

        try:
            # Verify the JWT signature and extract the user ID and email
            response = requests.get(
                f'https://www.googleapis.com/oauth2/v1/tokeninfo?id_token={id_token}')
            response.raise_for_status()
            user_id = response.json().get('sub', None)
            email = response.json().get('email', None)
        except requests.exceptions.RequestException:
            raise AuthenticationFailed('Failed to verify Google id_token')
        print(response.json())
        print("response.json()")
        return Response()
        # Authenticate the user based on the user ID or email
        # You can implement your own authentication logic here
        user = None
        if user_id:
            user = User.objects.filter(google_user_id=user_id).first()
        elif email:
            user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        return (user, None)


class GoogleJWTView(APIView):
    def post(self, request, *args, **kwargs):
        # id_token = request.META.get('HTTP_AUTHORIZATION', None)
        id_token = request.data.get('id_token', None)
        if not id_token:
            return None

        try:
            print('sdfsdf')
            # Verify the JWT signature and extract the user ID and email
            response = requests.get(
                f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={id_token}')
            response.raise_for_status()
        except Exception as e:
            print("!+++++++++=================")
            print(e)
            print("@+++++++++=================")
            raise AuthenticationFailed('Failed to verify Google id_token')
        print(response.json())
        print(response.json().get("user_id"))
        print(response.json().get("email"))
        print("response.json()")
        user_data = response.json()
        # Get or create user
        user, created = User.objects.get_or_create(
            email=user_data['email'])
        if created:
            user.username = user_data['email']
            user.set_unusable_password()
            user.save()


        # if user:
        refresh = TokenObtainPairSerializer.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        # Verify the Google access token and get the user ID and email
        # access_token = request.data.get('access_token')
        # user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        # headers = {'Authorization': f'Bearer {access_token}'}
        # response = requests.get(user_info_url, headers=headers)
        # response.raise_for_status()
        # user_info = response.json()
        # print(user_info)
        # print("user_info")
        # google_id = user_info.get('sub')
        # email = user_info.get('email')
        #
        # # Create or update the user with the Google ID and email
        # try:
        #     user = User.objects.get(google_id=google_id)
        #     user.email = email
        #     user.save()
        # except User.DoesNotExist:
        #     user = User.objects.create_user(email=email, google_id=google_id)
        #
        # # Generate a JWT token for the user
        # # serializer = JSONWebTokenSerializer(
        # #     data={'username': email, 'password': google_id})
        # # serializer.is_valid(raise_exception=True)
        # # token = serializer.object.get('token')
        # response_data = {'token': "token"}
        return Response(data, status=status.HTTP_200_OK)


class GoogleLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        adapter = GoogleOAuth2Adapter(request=request)
        provider = adapter.get_provider()
        access_token = self.request.data.get('access_token')
        token = provider.sociallogin_from_token({'access_token': access_token})
        user = token.user
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        })


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
