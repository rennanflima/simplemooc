from django.contrib import admin

from .models import Reply, Thread


# Register your models here.
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at']
    search_fields = ['title', 'author__email']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['thread', 'author', 'correct', 'created_at', 'updated_at']
    search_fields = ['thread__title', 'author__email', 'body']
