from rest_framework.generics import ListAPIView

from quizzes.api.serializers import NumberOfQuestionsSerializer
from quizzes.models import NumberOfQuestions


class ListNumberOfQuestionsView(ListAPIView):
    serializer_class = NumberOfQuestionsSerializer
    queryset = NumberOfQuestions.objects.all()


list_number_of_questions = ListNumberOfQuestionsView.as_view()
