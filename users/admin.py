from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display  = ('email', 'role', 'is_verified', 'is_staff', 'date_joined')
    list_filter   = ('role', 'is_verified', 'is_staff')
    ordering      = ('-date_joined',)

    # Override fieldsets to remove username, add our custom fields
    fieldsets = (
        (None,           {'fields': ('email', 'password')}),
        ('Profile',      {'fields': ('role', 'bio', 'avatar', 'is_verified')}),
        ('Permissions',  {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates',        {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2'),
        }),
    )