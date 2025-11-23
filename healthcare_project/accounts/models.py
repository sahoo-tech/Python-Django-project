from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Custom user model with email authentication"""

    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address_line = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email


class PatientProfile(models.Model):
    """Patient-specific information"""

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    medical_history = models.TextField(blank=True, help_text='Previous medical conditions')
    allergies = models.CharField(max_length=255, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"Patient: {self.user.get_full_name()}"


class DoctorProfile(models.Model):
    """Doctor-specific professional information"""

    SPECIALIZATION_CHOICES = (
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('general', 'General Practitioner'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    medical_license = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    professional_bio = models.TextField(blank=True)
    qualification = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.get_specialization_display()}"
