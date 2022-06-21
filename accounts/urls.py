from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (ChangePasswordView, ClientLoginView,
                    ForgotPasswordView, GenerateEmailOtpView, ValidateEmailOTPView,
                    GeneratePhoneOtpView, StaffLoginView, UserRegisterView,
                    ValidatePhoneOTPView,)

urlpatterns = [
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('forpass/', ForgotPasswordView.as_view()),
    path('otp-email/', GenerateEmailOtpView.as_view()),
    path('otp-email/validate/', ValidateEmailOTPView.as_view()),
    path('otp-phone/', GeneratePhoneOtpView.as_view()),
    path('otp-email/phone/', ValidatePhoneOTPView.as_view()),
    path('staff-login/', StaffLoginView.as_view()),
    path('client-login/', ClientLoginView.as_view()),  # Клиент вход
    path('pass-edit/', ChangePasswordView.as_view()),  # Пароль ауыстыру

]