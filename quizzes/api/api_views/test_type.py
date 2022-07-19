from rest_framework import generics

from quizzes.api.serializers import TestTypeSerializer
from quizzes.models import TestType


class TestTypeView(generics.ListAPIView):
    queryset = TestType.active_manager.all()
    serializer_class = TestTypeSerializer


test_type_view = TestTypeView.as_view()
