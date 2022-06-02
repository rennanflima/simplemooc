from django.contrib.auth.views import LoginView
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('entrar/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
]
