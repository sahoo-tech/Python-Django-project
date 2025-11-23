from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import CustomUser, PatientProfile, DoctorProfile
from .forms import SignUpForm, LoginForm, PatientProfileForm, DoctorProfileForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    if user.user_type == 'patient':
                        PatientProfile.objects.create(user=user)
                    elif user.user_type == 'doctor':
                        DoctorProfile.objects.create(user=user)
                    login(request, user)
                    messages.success(request, 'Account created successfully!')
                    return redirect('accounts:dashboard')
            except Exception as e:
                messages.error(request, f'Error: {e}')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}

    if user.user_type == 'patient':
        try:
            context['profile'] = user.patient_profile
        except PatientProfile.DoesNotExist:
            PatientProfile.objects.create(user=user)
            context['profile'] = user.patient_profile
        return render(request, 'accounts/patient_dashboard.html', context)

    elif user.user_type == 'doctor':
        try:
            context['profile'] = user.doctor_profile
            context['total_posts'] = user.blog_posts.count()
            context['published_posts'] = user.blog_posts.filter(status='published').count()
        except DoctorProfile.DoesNotExist:
            DoctorProfile.objects.create(user=user)
            context['profile'] = user.doctor_profile
            context['total_posts'] = 0
            context['published_posts'] = 0
        return render(request, 'accounts/doctor_dashboard.html', context)

    return redirect('accounts:login')


@login_required
def profile_update_view(request):
    user = request.user

    if user.user_type == 'patient':
        profile = user.patient_profile
        FormClass = PatientProfileForm
        template = 'accounts/patient_profile_update.html'
    else:
        profile = user.doctor_profile
        FormClass = DoctorProfileForm
        template = 'accounts/doctor_profile_update.html'

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.phone = request.POST.get('phone', user.phone)
            user.address_line = request.POST.get('address_line', user.address_line)
            user.city = request.POST.get('city', user.city)
            user.state = request.POST.get('state', user.state)
            user.pincode = request.POST.get('pincode', user.pincode)
            if 'profile_image' in request.FILES:
                user.profile_image = request.FILES['profile_image']
            user.save()
            messages.success(request, 'Profile updated!')
            return redirect('accounts:dashboard')
    else:
        form = FormClass(instance=profile)

    return render(request, template, {'form': form, 'user': user})
