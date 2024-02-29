from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from products.models import Course


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'author', 'title', 'start_date_time', 'cost', 'min_users', 'max_users', 'lessons_count')

    def get_lessons_count(self, obj):
        return obj.lessons.count()
