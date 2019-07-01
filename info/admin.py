from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from info.models import Info, MyUser, Token
from django.contrib.sessions.models import Session

from django.utils.translation import gettext_lazy as _


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'clinical_name', 'doc_name',
                    'doc_phone', 'sex_age', 'patient_phone')


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('phone', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'phone', 'is_staff')
    search_fields = ('username', 'phone', 'email')


admin.site.register(Session)
admin.site.register(Token)
