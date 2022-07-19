from accounts.api_views import serializers
from rest_framework import generics
from accounts import models


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer


user_register = UserRegistrationView.as_view()


class AddUserTestTypeView(generics.CreateAPIView):
    serializer_class = serializers.AddUserTestTypeSerializer


add_test_type = AddUserTestTypeView.as_view()
