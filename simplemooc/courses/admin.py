from re import A

from django.contrib import admin

from .models import Announcement, Comment, Course, Enrollment, Lesson, Material


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'start_date', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'course', 'release_date']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

    inlines = [MaterialInline]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'lesson']
    search_fields = ['name']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'status', 'created_at']
    search_fields = ['user__username', 'course__name']
    raw_id_fields = ['user', 'course']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'created_at']
    search_fields = ['course__name', 'title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'user', 'comment', 'created_at']
    search_fields = ['announcement__title', 'user__username', 'comment']
