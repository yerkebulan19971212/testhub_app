from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from base import abstract_serializer
from base.abstract_serializer import NameSerializer
from quizzes.models import (TestType, VariantGroup, Variant,
                            TestTypeLesson, Lesson, Answer, Question)


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
    answer_sign = serializers.CharField(source='answer_sign.name_code', read_only=True)

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


class GenerationQuestionByLessonSerializer(WritableNestedModelSerializer,
                                           serializers.ModelSerializer):
    answers = GenerationAnswerSerializer(many=True)
    choice_type = serializers.IntegerField(source='lesson_question_level.question_level.choice', read_only=True)
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)
    variant_group_name = serializers.CharField(source='variant_group.name_kz',  read_only=True)
    lesson_question_level = serializers.IntegerField(source='lesson_question_level.id', read_only=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'common_question',
            'lesson_question_level',
            'question',
            'created',
            'modified',
            'order',
            'is_active',
            'choice_type',
            'math',
            'variant_group_name',
            'created',
            'modified',
            'answers'
        )
