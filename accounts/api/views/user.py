from rest_framework import generics

from accounts.api import serializers


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer


user_register = UserRegistrationView.as_view()


class AddUserTestTypeView(generics.CreateAPIView):
    serializer_class = serializers.AddUserTestTypeSerializer


add_test_type = AddUserTestTypeView.as_view()
