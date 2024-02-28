from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Courses(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Описание')
    start_date_time = models.DateTimeField(verbose_name='Дата начала')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class CoursesAccess(models.Model):
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='students', verbose_name='Курс')
    students = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name='Студент')

    class Meta:
        verbose_name = 'Доступ к курсу'
        verbose_name_plural = 'Доступ к курсам'

    def __str__(self):
        return f'Студенту {self.students} доступен курс {self.courses}'


class Lesson(models.Model):
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    title = models.CharField(max_length=255, verbose_name='Название')
    video_link = models.URLField(verbose_name='Ссылка на видео')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='groups', verbose_name='Курс')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='users', verbose_name='Группа')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groups', verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Членство в группе'
        verbose_name_plural = 'Членство в группе'

    def __str__(self):
        return f'Студент {self.user}состоит в группе {self.group}'
