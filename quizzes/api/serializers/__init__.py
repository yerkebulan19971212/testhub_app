from .favorite import FavoritesSerializer
from .flash_cards import FlashCardsSerializer
from .lesson import (LessonNameSerializer, LessonSerializer,
                     LessonWithTestTypeLessonSerializer,
                     SaveLessonPairsForUserSerializer,
                     FullTestLessonSerializer,
                     FullTestFinishLessonSerializer)
from .number_of_questions import NumberOfQuestionsSerializer
from .pass_answer import FinishByLessonSerializer, PassAnswerSerializer
from .question import (QuestionsSerializer, FullTestQuestionSerializer,
                       FullTestFinishQuestionSerializer,
                       FullTestFinishQuestionByLessonSerializer)
from .quiz_event import (QuizEventInformationSerializer, QuizEventSerializer,
                         QuizSerializer, QuizTestPassAnswerSerializer)
from .tag import TagListSerializer
from .test_type import TestTypeOnlyNameSerializer, TestTypeSerializer
from .test_type_lesson import GetLessonTestTypeLessonSerializer
from .variants import UserVariantsSerializer, VariantGroupSerializer
from .full_test import (StudentAnswersSerializer, FinishFullTestSerializer,
                        GetFullTestResultSerializer, MarkSerializer)
from .info import (GradeSerializer, ComplainQuestionSerializer,
                   InfoErrorSerializer)
from .answer import (AnswerFinishedSerializer, )
from .universities import CountrySerializer, UniversityListSerializer, \
    UniversitySerializer
