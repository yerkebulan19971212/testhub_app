from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from accounts.api_views import views
from .api_views.views import update_user_information
# from rest_auth.views import LogoutView

from .views import (ChangePasswordView, ForgotPasswordView,
                    GenerateEmailOtpView, GeneratePhoneOtpView, StaffLoginView,
                    UploadAvatarView, UserRegisterView, ValidateEmailOTPView,
                    ValidatePhoneOTPView, GetSchemaView, student_login,
                    GoogleLoginView, GoogleJWTView, GoogleAuthentication,
                    student_login_by_phone, student_login_by_email
                    )

urlpatterns = [
# path('api/auth/', include('rest_auth.urls')),
    # path('api/auth/logout/', LogoutView.as_view(), name='rest_logout'),
    # path('api/auth/registration/', include('rest_auth.registration.urls')),
    # path('google/', include('allauth.urls')),
#
    path('google-login-2/', GoogleJWTView.as_view(), name='google_login'),
    # path('google-login/', GoogleLoginView.as_view(), name='google_login'),
    # path('google-login-3/', GoogleAuthentication.as_view(), name='google_login'),
    path('register-by-email/', views.user_register_by_email, name='register-by-email'),
    path('register-by-phone/', views.user_register_by_phone, name='register-by-phone'),
    path('me/', views.me_information, name='me_information'),
    path('add-test-type/', views.add_test_type),

    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('forpass/', ForgotPasswordView.as_view()),
    path('otp-email/', GenerateEmailOtpView.as_view()),
    path('otp-email/validate/', ValidateEmailOTPView.as_view()),
    path('otp-phone/', GeneratePhoneOtpView.as_view()),
    path('otp-email/phone/', ValidatePhoneOTPView.as_view()),
    path('staff-login/', StaffLoginView.as_view()),
    path('login/', student_login),
    path('login-phone/', student_login_by_phone),
    path('login-email/', student_login_by_email),
    path('avatar/<int:pk>/', UploadAvatarView.as_view()),
    path('pass-edit/', ChangePasswordView.as_view()),  # Пароль ауыстыру
    path('update/', update_user_information),
    path('supdate/', GetSchemaView.as_view())
]
