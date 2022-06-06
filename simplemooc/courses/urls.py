from django.urls import path

from simplemooc.courses.views import announcements, details, enrollment, index, lessons, material, show_announcement, show_lesson, undo_enrollment

app_name = 'courses'
urlpatterns = [
    path('', index, name='index'),
    path('<slug:slug>/', details, name='details'),
    path('<slug:slug>/inscricao/', enrollment, name='enrollment'),
    path('<slug:slug>/cancelar-inscricao/', undo_enrollment, name='undo_enrollment'),
    path('<slug:slug>/anuncios/', announcements, name='announcements'),
    path('<slug:slug>/anuncios/<int:pk>/', show_announcement, name='show_announcement'),
    path('<slug:slug>/aulas/', lessons, name='lessons'),
    path('<slug:slug>/aulas/<int:pk>/', show_lesson, name='show_lesson'),
    path('<slug:slug>/aulas/<int:lesson_id>/material/<int:pk>/', material, name='material'),
]
