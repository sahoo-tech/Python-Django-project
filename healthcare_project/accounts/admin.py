from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PatientProfile, DoctorProfile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'user_type', 'is_staff']
    list_filter = ['user_type', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal', {'fields': ('first_name', 'last_name', 'phone', 'profile_image')}),
        ('Address', {'fields': ('address_line', 'city', 'state', 'pincode')}),
        ('Type', {'fields': ('user_type',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
