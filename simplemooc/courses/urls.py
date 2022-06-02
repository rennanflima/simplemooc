from django.urls import path
from simplemooc.courses.views import details, index

app_name = 'courses'
urlpatterns = [
    path('', index, name='index'),
    path('<slug:slug>/', details, name='details'),
]
