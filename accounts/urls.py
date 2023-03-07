from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.api_views import views

from .api_views.views import update_user_information
from .views import (ChangePasswordView, ForgotPasswordView,
                    GenerateEmailOtpView, GeneratePhoneOtpView, GetSchemaView,
                    GoogleJWTView, StaffLoginView, UploadAvatarView,
                    ValidateEmailOTPView, ValidatePhoneOTPView, my_progress,
                    student_login, student_login_by_email,
                    student_login_by_phone)

urlpatterns = [
    path('google-login-2/', GoogleJWTView.as_view(), name='google_login'),
    path('register-by-email/', views.user_register_by_email),
    path('register-by-phone/', views.user_register_by_phone),
    path('me/', views.me_information, name='me_information'),
    path('add-test-type/', views.add_test_type),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forpass/', ForgotPasswordView.as_view()),
    path('otp-email/', GenerateEmailOtpView.as_view()),
    path('otp-email/validate/', ValidateEmailOTPView.as_view()),
    path('otp-phone/', GeneratePhoneOtpView.as_view()),
    path('otp-email/phone/', ValidatePhoneOTPView.as_view()),
    path('staff-login/', StaffLoginView.as_view()),
    # path('login/', student_login),
    path('login-phone/', student_login_by_phone),
    path('login-email/', student_login_by_email),
    path('avatar/<int:pk>/', UploadAvatarView.as_view()),
    path('pass-edit/', ChangePasswordView.as_view()),
    path('update/', update_user_information),
    path('supdate/', GetSchemaView.as_view()),
    path('my-progress/', my_progress)
]
