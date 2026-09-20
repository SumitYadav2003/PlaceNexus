from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    register_view,
    login_view,
    logout_view,
    home_view,
    student_dashboard_view,
    coordinator_dashboard_view,
    profile_view,
    edit_profile_view,
    student_profile_view,
    coordinator_profile_view
    
)

urlpatterns = [
    path('', home_view, name='home'),

    path(
        'register/',
        register_view,
        name='register'
    ),

    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'profile/',
        profile_view,
        name='profile'
    ),
    
    path(
    'student/<int:profile_id>/',
    student_profile_view,
    name='student_profile'
),
    
    path(
        'profile/edit/',
        edit_profile_view,
        name='edit_profile'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'student-dashboard/',
        student_dashboard_view,
        name='student_dashboard'
    ),

    path(
        'coordinator-dashboard/',
        coordinator_dashboard_view,
        name='coordinator_dashboard'
    ),
    
    path(
    'coordinator/<int:profile_id>/',
    coordinator_profile_view,
    name='coordinator_profile'
),
    
    path(
    "employer-dashboard/",
    views.employer_dashboard_view,
    name="employer_dashboard",
),
    # ---------------- Password Reset ----------------

path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html",
        email_template_name="accounts/password_reset_email.html",
        subject_template_name="accounts/password_reset_subject.txt",
        success_url="/password-reset/done/",
    ),
    name="password_reset",
),

path(
    "password-reset/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ),
    name="password_reset_done",
),

path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
        success_url="/reset/done/",
    ),
    name="password_reset_confirm",
),

path(
    "reset/done/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ),
    name="password_reset_complete",
),
path(

    "verify-otp/",

    views.verify_otp_view,

    name="verify_otp",

),
path(
    "resend-otp/",
    views.resend_otp_view,
    name="resend_otp",
),
path(
    "deactivate-account/",
    views.deactivate_account_view,
    name="deactivate_account",
),
path(
    "permanent-deactivate/",
    views.permanent_deactivate_account_view,
    name="permanent_deactivate_account",
),
path(

    "coordinator-placement-requests/",

    views.coordinator_requests_view,

    name="coordinator_requests",

),
path(
    "employer-analytics/",
    views.employer_analytics_view,
    name="employer_analytics",
),
]