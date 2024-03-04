from django.contrib import admin

from .models import Course, Lesson, Cohort, CohortMembership


class CohortAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_name')
    list_select_related = ('course',)

    def course_name(self, obj):
        return obj.course.title

    course_name.short_description = 'Название курса'


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'start_date_time', 'max_users')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_name')

    def course_name(self, obj):
        return obj.courses.title

    course_name.short_description = 'Название курса'


class CohortMembershipAdmin(admin.ModelAdmin):
    list_display = ('cohort', 'student')


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Cohort, CohortAdmin)
admin.site.register(CohortMembership, CohortMembershipAdmin)
