from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from quizzes.api.serializers import QuestionsSerializer
from quizzes.models import Question



class QuestionsListView(generics.ListAPIView):
    queryset = Question.objects.all().order_by('-id')[:20]
    serializer_class = QuestionsSerializer
    permission_classes = (IsAuthenticated,)


questions_list = QuestionsListView.as_view()
