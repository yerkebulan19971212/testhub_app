from django.db.models import Count
from rest_framework import serializers

from base import abstract_serializer
from quizzes.models import Lesson, LessonGroup, UserVariant, TestTypeLesson


class LessonSerializer(abstract_serializer.NameSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
            'icon',
            'chosen_icon'
        )


class LessonNameSerializer(abstract_serializer.NameSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'name'
        )


class LessonWithTestTypeLessonSerializer(abstract_serializer.NameSerializer):
    test_type_lesson_id = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            # 'id',
            'name',
            'icon',
            'chosen_icon',
            'test_type_lesson_id'
        )

    @staticmethod
    def get_test_type_lesson_id(obj):
        return obj.test_type_lessons.all()[0].id


class SaveLessonPairsForUserSerializer(serializers.ModelSerializer):
    lessons = serializers.ListField(child=serializers.IntegerField(),
                                    required=True, min_length=2, max_length=2)

    class Meta:
        model = UserVariant
        fields = ('lessons',)

    def update(self, instance, validated_data):
        lessons = validated_data.get('lessons')

        lesson_group = LessonGroup.objects.filter(
            lesson_pairs__lesson_id__in=lessons
        ).annotate(lesson_count=Count('lesson_pairs__lesson_id')).filter(
            lesson_count=2
        ).first()
        validated_data['lesson_group'] = lesson_group
        return super().update(instance, validated_data)


class FullTestLessonSerializer(serializers.ModelSerializer):
    number_of_questions = serializers.IntegerField(default=0)
    number_of_score = serializers.IntegerField(default=0)
    my_score = serializers.IntegerField(default=0)
    icon = serializers.ImageField(source='lesson.icon')
    chosen_icon = serializers.ImageField(source='lesson.chosen_icon')
    name = serializers.SerializerMethodField()

    class Meta:
        model = TestTypeLesson
        fields = (
            'id',
            'name',
            'language',
            'main',
            'number_of_questions',
            'number_of_score',
            'my_score',
            'icon',
            'chosen_icon'
        )

    def get_name(self, obj):
        language = self.context.get('request').headers.get('language', 'kz')
        if language == 'kz':
            return obj.lesson.name_kz
        return obj.lesson.name_ru

class FullTestFinishLessonSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = TestTypeLesson
        fields = (
            'id',
            'name',
            'language',
            'main',
        )

    def get_name(self, obj):
        language = self.context.get('request').headers.get('language', 'kz')
        if language == 'kz':
            return obj.lesson.name_kz
        return obj.lesson.name_ru
