from rest_framework import serializers

from .models import Course, Lesson, Payment
from .validators import validate_url


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.URLField(validators=[validate_url])

    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ("id",)


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ("id",)

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе"""
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
