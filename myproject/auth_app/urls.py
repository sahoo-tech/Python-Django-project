from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/edit-profile/', views.edit_patient_profile, name='edit_patient_profile'),
    path('doctor/edit-profile/', views.edit_doctor_profile, name='edit_doctor_profile'),
]
