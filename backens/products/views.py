from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import Course, CohortMembership, Lesson
from products.serializers import CourseSerializer, LessonSerializer

User = get_user_model()


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def lessons(self, request, slug):
        course = get_object_or_404(Course, slug=slug)

        if not CohortMembership.objects.filter(student=request.user, cohort__course=course).exists():
            return Response({'error': 'Вы не приобрели данный курс'}, status=status.HTTP_403_FORBIDDEN)

        lessons = Lesson.objects.filter(courses=course)
        serializer = LessonSerializer(lessons, many=True)

        return Response(serializer.data)

