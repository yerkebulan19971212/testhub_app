from rest_framework import generics
from rest_framework.views import APIView

from quizzes.api.serializers import test_serializers
from quizzes.models import *


class TestTypeView(generics.ListAPIView):
    queryset = test_type.TestType.objects.filter(is_active=True).order_by('order')
    serializer_class = test_serializers.TestTypeSerializer
