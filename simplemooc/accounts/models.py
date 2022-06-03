import re

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.core import validators
from django.db import models


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('nome de usuário', max_length=30, unique=True,
                                validators=[validators.RegexValidator(re.compile('^[\\w.@+-]+$'),
                                                                      'O nome de usuário só pode conter letras, digitos ou os seguintes caracteres: @/./+/-/_',
                                                                      'invalid')])
    email = models.EmailField('e-mail', unique=True)
    name = models.CharField('nome', max_length=150, blank=True)
    is_active = models.BooleanField('está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('é da equipe?', blank=True, default=False)
    date_joined = models.DateTimeField('data de entrada', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)
