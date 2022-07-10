from rest_framework import generics
from rest_framework.views import APIView
from quizzes.models import *
from quizzes.api.serializers import test_serializers


class TestTypeView(generics.ListAPIView):
    queryset = test_type.TestType.objects.filter(is_active=True).order_by('order')
    serializer_class = test_serializers.TestTypeSerializer
