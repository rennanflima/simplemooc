from re import A

from django.contrib import admin

from .models import Announcement, Comment, Course, Enrollment


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'start_date', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'status', 'created_at']
    search_fields = ['user__username', 'course__name']
    raw_id_fields = ['user', 'course']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'created_at']
    search_fields = ['course__name', 'title']
    raw_id_fields = ['course']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'user', 'comment', 'created_at']
    search_fields = ['announcement__title', 'user__username', 'comment']
    raw_id_fields = ['announcement', 'user']
