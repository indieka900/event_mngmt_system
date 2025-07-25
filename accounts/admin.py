from django.contrib import admin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture')
        }),
        (_('Permissions'), {
            'fields': ('user_type', 'is_staff', 'is_active')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type')
        }),
    )
    
