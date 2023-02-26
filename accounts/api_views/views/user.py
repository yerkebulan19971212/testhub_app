from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api_views import serializers
from accounts.api_views.serializers import (MeInformationSerializer,
                                            UserInformationUpdateSerializer)
from accounts.models import User


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        phone = request.data.get('phone')
        result = {
            "phone": True,
            "email": True
        }
        data = {
            "status": True,
            "message": "Success",
            "status_code": 0,
            "result": None,
        }
        if User.objects.filter(phone=phone).exists():
            result["phone"] = False
        if User.objects.filter(email=email).exists():
            result["email"] = False
        if result["phone"] is False or result["email"] is False:
            data["result"] = result
            data["status"] = False
            data["message"] = "Fail"
            data["status_code"] = 9001
        else:
            data = self.create(request, *args, **kwargs).data
        return Response(data, status=status.HTTP_200_OK)


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
