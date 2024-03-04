from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
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

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def buy(self, request, slug):
        course = get_object_or_404(Course, slug=slug)

        user = request.user
        cohorts = course.cohorts.prefetch_related('users').all()

        if not cohorts.exists():
            return Response({'message': 'Для данного курса еще нет когорт'}, status=status.HTTP_403_FORBIDDEN)

        if CohortMembership.objects.filter(student=user, cohort__course=course).exists():
            return Response({'error': 'Вы уже приобрели данный курс'}, status=status.HTTP_403_FORBIDDEN)

        if course.start_date_time < timezone.now():
            return Response(
                {'message': 'Вы опоздали на данный курс, он уже начался'},
                status=status.HTTP_403_FORBIDDEN
            )

        all_users = cohorts.aggregate(total_users=Count('users__id', distinct=True))['total_users']
        cohorts_count = len(cohorts)
        if all_users < course.min_users * cohorts_count:
            for cohort in cohorts:
                if cohort.users.count() < course.min_users:
                    CohortMembership.objects.create(cohort=cohort, student=user)
                    message = (f'Поздравляем! Вы успешно приобрели курс: "{course.title}"'
                               f' и зачислены в когорту: "{cohort.title}"')
                    return Response({'message': message}, status=status.HTTP_200_OK)
        elif all_users < course.max_users * cohorts_count:
            index = all_users % len(cohorts)
            CohortMembership.objects.create(cohort=cohorts[index], student=user)
            message = (f'Поздравляем! Вы успешно приобрели курс: "{course.title}"'
                       f' и зачислены в когорту: "{cohorts[index].title}"')
            return Response({'message': message}, status=status.HTTP_200_OK)

        return Response(
            {'message': 'Извините, все когорты для данного курса заполнены. Дождитесь следующего набора'},
            status=status.HTTP_403_FORBIDDEN
        )
