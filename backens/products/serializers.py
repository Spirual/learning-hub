from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from products.models import Course, Lesson

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class CourseSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    lessons_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'author', 'title', 'slug', 'start_date_time', 'cost', 'min_users', 'max_users', 'lessons_count')

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'video_link')
