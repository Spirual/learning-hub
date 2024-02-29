from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Course(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_courses', verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Описание')
    start_date_time = models.DateTimeField(verbose_name='Дата начала')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    min_users = models.PositiveIntegerField(default=1, verbose_name='Мин. кол-во студентов')
    max_users = models.PositiveIntegerField(default=20, verbose_name='Макc. кол-во студентов')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class CourseAccess(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students', verbose_name='Курс')
    students = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='students_courses',
        verbose_name='Студент',
    )

    class Meta:
        verbose_name = 'Доступ к курсу'
        verbose_name_plural = 'Доступ к курсам'

    def __str__(self):
        return f'Доступ студента {self.students} к курсу {self.courses}'


class Lesson(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    title = models.CharField(max_length=255, verbose_name='Название')
    video_link = models.URLField(verbose_name='Ссылка на видео')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Cohort(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cohorts', verbose_name='Курс')

    class Meta:
        verbose_name = 'Когорта'
        verbose_name_plural = 'Когорты'

    def __str__(self):
        return self.title


class CohortMembership(models.Model):
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='users', verbose_name='Когорта')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cohorts', verbose_name='Студент')

    class Meta:
        verbose_name = 'Членство в когорте'
        verbose_name_plural = 'Членства в когорте'

    def __str__(self):
        return f'Членство студента {self.student} в когорте {self.cohort}'
