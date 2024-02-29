from django.contrib.auth import get_user_model
from rest_framework import viewsets

from products.models import Course
from products.serializers import CourseSerializer

User = get_user_model()


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


