from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, PatientProfile, DoctorProfile


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Custom user admin."""

    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'user_type', 'is_active', 'created_at'
    )
    list_filter = ('user_type', 'is_active', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Information', {
            'fields': (
                'user_type', 'profile_picture', 'address_line1',
                'city', 'state', 'pincode'
            )
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Information', {
            'fields': (
                'user_type', 'address_line1',
                'city', 'state', 'pincode'
            )
        }),
    )


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    """Patient profile admin."""

    list_display = ('user', 'blood_group', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Medical Information', {
            'fields': ('medical_history', 'allergies', 'blood_group')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    """Doctor profile admin."""

    list_display = (
        'user', 'specialization', 'experience_years',
        'consultation_fee', 'created_at'
    )
    list_filter = ('specialization', 'created_at')
    search_fields = ('user__email', 'license_number', 'user__first_name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Professional Information', {
            'fields': (
                'specialization', 'license_number',
                'experience_years', 'consultation_fee', 'bio'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
