from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from .forms import RegisterForm
from .models import User

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'is_staff')
    search_fields = ('username', 'name', 'email')
    add_form = RegisterForm
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    actions = ['activate_register', 'deactivate_register']

    def activate_register(self, request, queryset):
        """Ação para ativar usuários selecionados."""
        count = queryset.update(is_active=True)
        if count == 1:
            msg = '{} usuário foi ativado.'
        else:
            msg = '{} usuários foram ativados.'

        self.message_user(request, msg.format(count))

    activate_register.short_description = 'Ativar usuários selecionados'

    def deactivate_register(self, request, queryset):
        """Ação para desativar usuários selecionados."""
        count = queryset.update(is_active=False)

        if count == 1:
            msg = '{} usuário foi desativado.'
        else:
            msg = '{} usuários foram desativados.'

        self.message_user(request, msg.format(count))

    deactivate_register.short_description = 'Desativar usuários selecionados'
