from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import Coalesce
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
    students_count = SerializerMethodField()
    group_fill = SerializerMethodField()
    acquisition_percentage = SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'author', 'title', 'slug', 'start_date_time', 'cost', 'min_users', 'max_users', 'lessons_count', 'students_count', 'group_fill', 'acquisition_percentage')

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_students_count(self, obj):
        return obj.cohorts.aggregate(total_students=Count('users__id', distinct=True))['total_students']

    def get_group_fill(self, obj):
        max_users = obj.max_users
        cohorts_count = obj.cohorts.count()
        total_students = obj.cohorts.aggregate(total_students=Count('users__id', distinct=True))['total_students']

        if cohorts_count > 0:
            average_group_size = total_students / cohorts_count
            fill_percentage = (average_group_size / max_users) * 100
            return round(fill_percentage, 2)
        else:
            return 0

    def get_acquisition_percentage(self, obj):
        total_users_on_platform = User.objects.count()
        total_accesses = obj.cohorts.aggregate(total_accesses=Coalesce(Count('users__id', distinct=True), 0))['total_accesses']

        if total_users_on_platform > 0:
            acquisition_percentage = (total_accesses / total_users_on_platform) * 100
            return round(acquisition_percentage, 2)
        else:
            return 0


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'video_link')
