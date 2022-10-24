from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.api_views import serializers
from accounts.api_views.serializers import (MeInformationSerializer,
                                            UserInformationUpdateSerializer)
from accounts.models import User


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer


user_register = UserRegistrationView.as_view()


class AddUserTestTypeView(generics.CreateAPIView):
    serializer_class = serializers.AddUserTestTypeSerializer


add_test_type = AddUserTestTypeView.as_view()


class MeInformationView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = MeInformationSerializer

    def get_object(self):
        return self.request.user


me_information = MeInformationView.as_view()


class UserInformationUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserInformationUpdateSerializer
    lookup_field = None

    def get_object(self):
        return self.request.user


update_user_information = UserInformationUpdateView.as_view()
