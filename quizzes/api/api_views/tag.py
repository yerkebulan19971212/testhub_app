from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from quizzes.api.serializers import TagListSerializer
from quizzes.filters import TagFilter
from quizzes.models import Tag


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.select_related('test_type_lesson').all()
    serializer_class = TagListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TagFilter


tag_list_view = TagListView.as_view()