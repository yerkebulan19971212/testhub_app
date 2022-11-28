from django.db.models import Count
from rest_framework import serializers

from base import abstract_serializer
from quizzes.models import Lesson, LessonGroup, UserVariant


class LessonSerializer(abstract_serializer.NameSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
            'icon',
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
        ).annotate(lesson_count=Count('id')).filter(
            lesson_count__lt=2
        ).first()
        validated_data['lesson_group'] = lesson_group
        return super().update(instance, validated_data)
