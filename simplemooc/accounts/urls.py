from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path, re_path, reverse_lazy

from .views import dashboard, edit, edit_password, register

app_name = 'accounts'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('entrar/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('sair/', LogoutView.as_view(next_page='core:home'), name='logout'),
    path('cafastre-se/', register, name='register'),
    path('editar/', edit, name='edit'),
    path('editar-senha/', edit_password, name='edit_password'),
    path('redefinicao-senha/', PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
                                                         subject_template_name='accounts/password_reset_subject.txt',
                                                         email_template_name='accounts/password_reset_email.html',
                                                         success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    path('redefinicao-senha/enviada/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('redefinicao-senha/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',
                                                                                 success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('redefinicao_senha/completada/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
