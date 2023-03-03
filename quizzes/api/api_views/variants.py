from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from quizzes.api.serializers import (SaveLessonPairsForUserSerializer,
                                     UserVariantsSerializer,
                                     VariantGroupSerializer)
from quizzes.filters import UserVariantFilter, VariantGroupFilter
from quizzes.models import UserVariant, VariantGroup


class VariantGroupsView(generics.ListAPIView):
    serializer_class = VariantGroupSerializer
    queryset = VariantGroup.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_class = VariantGroupFilter


variant_groups = VariantGroupsView.as_view()


class UserVariantsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserVariantsSerializer
    queryset = UserVariant.objects.select_related(
        'variant',
        'variant__variant_group'
    ).all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserVariantFilter

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(user=user)
        return queryset.order_by('variant__variant')


user_variants_list = UserVariantsView.as_view()


class UserVariantsCountView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserVariantsSerializer
    queryset = UserVariant.objects.select_related(
        'variant',
        'variant__variant_group'
    ).all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserVariantFilter

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset())
        active_count = queryset.filter(user=user).count()
        return Response({"result": active_count})


user_variants_list_count = UserVariantsCountView.as_view()


class SaveLessonPairsForUserView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserVariant.objects.all()
    serializer_class = SaveLessonPairsForUserSerializer
    lookup_field = 'pk'
    http_method_names = ['patch']


save_lesson_pairs = SaveLessonPairsForUserView.as_view()
