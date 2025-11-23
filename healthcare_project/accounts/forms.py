from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, PatientProfile, DoctorProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter email'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'First name'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Last name'
    }))
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'user_type', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter password'
    }))


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['medical_history', 'allergies', 'blood_group', 'date_of_birth', 'emergency_contact']
        widgets = {
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'allergies': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'medical_license', 'years_of_experience', 
                  'consultation_fee', 'professional_bio', 'qualification']
        widgets = {
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'medical_license': forms.TextInput(attrs={'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'professional_bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
        }
