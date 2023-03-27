from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from base import abstract_serializer
from base.abstract_serializer import NameSerializer
from quizzes.models import (TestType, VariantGroup, Variant,
                            TestTypeLesson, Lesson, Answer, Question,
                            CommonQuestion, LessonQuestionLevel, QuestionLevel,
                            Topic, TopicQuestion, AnswerSign)


class GenerationLessonSerializer(abstract_serializer.NameSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
            'name_kz',
            'name_ru',
            'name_en',
            'is_active',
            'order',
            'icon',
            'chosen_icon',
            'math',
            'created',
            'modified'
        )


class GenerationTestTypeSerializer(NameSerializer):
    class Meta:
        model = TestType
        fields = (
            'id',
            'name',
            'name_kz',
            'name_ru',
            'name_en',
            'is_active',
            'name_code',
            'order',
            'icon',
            'created',
            'modified'
        )


class GenerationVariantGroupSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)

    class Meta:
        model = VariantGroup
        fields = (
            'id',
            'name_kz',
            'name_ru',
            'name_en',
            'is_active',
            'name_code',
            'order',
            'icon',
            'test_type',
            'duration',
            'created',
            'modified'
        )


class GenerationVariantListSerializer(NameSerializer):
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Variant
        fields = (
            'id',
            'variant',
            'variant_group',
            'sum_question',
            'main',
            'is_active',
            'order',
            'created',
            'modified'
        )


class GenerationGetLessonTestTypeLessonSerializer(serializers.ModelSerializer):
    test_type = GenerationTestTypeSerializer()
    lesson = GenerationLessonSerializer()
    number_of_questions = serializers.IntegerField(default=0)

    class Meta:
        model = TestTypeLesson
        fields = (
            'id',
            'lesson',
            'language',
            'test_type',
            'main',
            'number_of_questions',
            'questions_number'
        )


class GenerationAnswerSerializer(serializers.ModelSerializer):
    answer_sign = serializers.CharField(source='answer_sign.name_code',
                                        read_only=True)

    class Meta:
        model = Answer
        fields = (
            'id',
            'question',
            'answer',
            'correct',
            'math',
            'answer_sign'
        )


class GenerationCommonQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonQuestion
        fields = (
            'id',
            'name_code',
            'file',
            'text'
        )


class AnswerSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerSign
        field = (
            'id'
        )


class GenerationCreateSerializer(serializers.ModelSerializer):
    # answer_sign = serializers.IntegerField(required=False)

    class Meta:
        model = Answer
        fields = (
            'id',
            'answer',
            'correct',
            'math',
            'answer_sign'
        )

    def create(self, validated_data):
        print(validated_data)
        print("validated_data")
        return super().create(validated_data)


class GenerationQuestionByLessonSerializer(WritableNestedModelSerializer,
                                           serializers.ModelSerializer):
    answers = GenerationCreateSerializer(many=True)
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)
    topic_id = serializers.IntegerField(write_only=True, required=True)
    question_order= serializers.IntegerField(source='var')

    class Meta:
        model = Question
        fields = (
            'id',
            'common_question',
            'lesson_question_level',
            'question',
            'topic_id',
            'created',
            'modified',
            'is_active',
            'math',
            'variant_group',
            'created',
            'modified',
            'answers'
        )

    def create(self, validated_data):
        topic_id = validated_data.pop('topic_id')
        answer_signs = list(AnswerSign.objects.all().order_by('order'))
        for i, ans in enumerate(validated_data['answers']):
            ans['answer_sign'] = answer_signs[i].id
            print(ans)
            print(answer_signs[i].id)
        print(validated_data)
        print("validated_data")
        question = super().create(validated_data)
        TopicQuestion.objects.create(
            question=question,
            topic_id=topic_id
        )

        return question


class GenerationListQuestionByLessonSerializer(
    GenerationQuestionByLessonSerializer):
    common_question = GenerationCommonQuestionSerializer()


class GenerationQuestionLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionLevel
        fields = (
            'id',
            'name_code'
        )


class GenerationLessonQuestionLevelSerializer(serializers.ModelSerializer):
    name_code = serializers.CharField(source='question_level.name_code')

    class Meta:
        model = LessonQuestionLevel
        fields = (
            'id',
            'test_type_lesson',
            'name_code'
        )


class TopicSerializer(abstract_serializer.NameSerializer):
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Topic
        fields = (
            'id',
            'name',
            'name_kz',
            'name_ru',
            'name_en',
            'is_active',
            'name_code',
            'order',
            'test_type_lesson',
            'created',
            'modified'
        )


class ImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    group_id = serializers.IntegerField()
    level_id = serializers.IntegerField()
    topic_id = serializers.IntegerField()


class GenerationSerializer(serializers.Serializer):
    unique_percent = serializers.IntegerField(required=True)
    variant_group = serializers.IntegerField(required=True)
    # variant_list = serializers.ListField(
    #     child=serializers.IntegerField(),
    #     required=True
    # )
