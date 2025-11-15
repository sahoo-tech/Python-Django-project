from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import CustomUser, PatientProfile, DoctorProfile
from .forms import (
    CustomUserSignUpForm,
    CustomUserLoginForm,
    PatientProfileForm,
    DoctorProfileForm
)


def signup_view(request):
    """Handle user signup."""

    # Redirect if already logged in
    if request.user.is_authenticated:
        if request.user.user_type == 'patient':
            return redirect('auth:patient_dashboard')
        else:
            return redirect('auth:doctor_dashboard')

    if request.method == 'POST':
        form = CustomUserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Create user
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()

                # Create related profile
                if user.user_type == 'patient':
                    PatientProfile.objects.create(user=user)
                elif user.user_type == 'doctor':
                    DoctorProfile.objects.create(user=user)

                messages.success(
                    request,
                    'Account created successfully! Please login.'
                )
                return redirect('auth:login')

            except IntegrityError as e:
                messages.error(request, 'Error creating account. Please try again.')
                form.add_error(None, str(e))
        else:
            # Form has errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserSignUpForm()

    return render(request, 'auth/signup.html', {'form': form})


def login_view(request):
    """Handle user login."""

    # Redirect if already logged in
    if request.user.is_authenticated:
        if request.user.user_type == 'patient':
            return redirect('auth:patient_dashboard')
        else:
            return redirect('auth:doctor_dashboard')

    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Authenticate user
            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!')

                    # Redirect to dashboard based on user type
                    if user.user_type == 'patient':
                        return redirect('auth:patient_dashboard')
                    else:
                        return redirect('auth:doctor_dashboard')
                else:
                    messages.error(request, 'Account is inactive.')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = CustomUserLoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('auth:login')


@login_required(login_url='auth:login')
def patient_dashboard(request):
    """Patient dashboard view."""

    # Check if user is patient
    if request.user.user_type != 'patient':
        messages.error(request, 'Access denied. This page is for patients only.')
        return redirect('auth:home')

    try:
        patient_profile = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        patient_profile = PatientProfile.objects.create(user=request.user)

    context = {
        'user': request.user,
        'patient_profile': patient_profile
    }
    return render(request, 'dashboard/patient_dashboard.html', context)


@login_required(login_url='auth:login')
def doctor_dashboard(request):
    """Doctor dashboard view."""

    # Check if user is doctor
    if request.user.user_type != 'doctor':
        messages.error(request, 'Access denied. This page is for doctors only.')
        return redirect('auth:home')

    try:
        doctor_profile = DoctorProfile.objects.get(user=request.user)
    except DoctorProfile.DoesNotExist:
        doctor_profile = DoctorProfile.objects.create(user=request.user)

    context = {
        'user': request.user,
        'doctor_profile': doctor_profile
    }
    return render(request, 'dashboard/doctor_dashboard.html', context)


@login_required(login_url='auth:login')
def edit_patient_profile(request):
    """Edit patient profile view."""

    # Check if user is patient
    if request.user.user_type != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('auth:home')

    try:
        patient_profile = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        patient_profile = PatientProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('auth:patient_dashboard')
    else:
        form = PatientProfileForm(instance=patient_profile)

    context = {'form': form, 'patient_profile': patient_profile}
    return render(request, 'dashboard/edit_patient_profile.html', context)


@login_required(login_url='auth:login')
def edit_doctor_profile(request):
    """Edit doctor profile view."""

    # Check if user is doctor
    if request.user.user_type != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('auth:home')

    try:
        doctor_profile = DoctorProfile.objects.get(user=request.user)
    except DoctorProfile.DoesNotExist:
        doctor_profile = DoctorProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('auth:doctor_dashboard')
    else:
        form = DoctorProfileForm(instance=doctor_profile)

    context = {'form': form, 'doctor_profile': doctor_profile}
    return render(request, 'dashboard/edit_doctor_profile.html', context)


def home_view(request):
    """Home page view."""

    # Redirect if already logged in
    if request.user.is_authenticated:
        if request.user.user_type == 'patient':
            return redirect('auth:patient_dashboard')
        else:
            return redirect('auth:doctor_dashboard')

    return render(request, 'home.html')
