from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from applications.models import Interview
from datetime import date, timedelta
from .forms import RegisterForm
from profiles.models import Profile
from profiles.forms import ProfileForm
from applications.models import Application
from placements.models import Placement,PlacementRequest
from applications.models import SavedPlacement,SupportTicket
from django.contrib.messages import get_messages
from applications.models import CommunityPost
import time 
from .utils import send_login_otp, is_demo_account
from applications.models import (
    CommunityPost,
    Application,
)

from django.db.models import Count



def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.email = form.cleaned_data["email"]

            user.save()

            role = form.cleaned_data["role"]

            Profile.objects.create(

                user=user,

                role=role,

            )

            messages.success(

                request,

                "Account created successfully."

            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(

        request,

        "accounts/register.html",

        {

            "form": form,

        },

    )
    
from django.core.mail import send_mail
from random import randint
def login_view(request):

    # Clear old messages
    storage = get_messages(request)

    for _ in storage:
        pass

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(

            request,

            username=username,

            password=password,

        )

        if user is not None:

            profile = Profile.objects.get(
            user=user
)

# Permanent deactivation
            if profile.is_permanently_deactivated:

                messages.error(

                    request,

                    "This account has been permanently deactivated. Please contact the administrator."

    )

                return redirect("login")

# Temporary deactivation
            if not profile.is_account_active:

                profile.is_account_active = True

                profile.save()

                messages.success(

                    request,

                    "Welcome back! Your account has been reactivated."

    )

            # Demo accounts (see DEMO_ACCOUNTS setting) skip the emailed OTP
            if is_demo_account(user):

                login(request, user)

                if profile.role == "student":
                    return redirect("student_dashboard")

                if profile.role == "coordinator":
                    return redirect("coordinator_dashboard")

                return redirect("employer_dashboard")

            send_login_otp(

                user,

                request

            )

            return redirect("verify_otp")

        else:

            messages.error(

                request,

                "Invalid username or password."

            )

    return render(

        request,

        "login.html",

    )
    

@login_required
def deactivate_account_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if request.method == "POST":

        profile.is_account_active = False

        profile.save()

        logout(request)

        messages.success(

            request,

            "Your account has been temporarily deactivated."

        )

        return redirect("home")

    return render(

        request,

        "accounts/deactivate_account.html"
    )



@login_required
def permanent_deactivate_account_view(request):

    if is_demo_account(request.user):

        messages.error(
            request,
            "Demo accounts cannot be permanently deactivated."
        )

        return redirect("home")

    profile = Profile.objects.get(
        user=request.user
    )

    if request.method == "POST":

        profile.is_account_active = False

        profile.is_permanently_deactivated = True

        profile.save()

        logout(request)

        messages.success(

            request,

            "Your account has been permanently deactivated."

        )

        return redirect("home")

    return render(

        request,

        "accounts/permanent_deactivate_account.html"
    )

from django.contrib.auth import login
from django.utils import timezone
def verify_otp_view(request):

    if "otp" not in request.session:

        return redirect("login")

    remaining = max(

        0,

        300 -

        (

            int(time.time())

            -

            request.session.get(

                "otp_created",

                0

            )

        )

    )

    if remaining == 0:

        request.session.pop("otp",None)

        request.session.pop("otp_user",None)

        request.session.pop("otp_created",None)

        messages.error(

            request,

            "OTP expired."

        )

        return redirect("login")

    if request.method=="POST":

        otp=request.POST.get("otp")

        if otp==request.session["otp"]:

            from django.contrib.auth.models import User

            user=User.objects.get(

                id=request.session["otp_user"]

            )

            login(

                request,

                user

            )

            request.session.pop("otp",None)

            request.session.pop("otp_user",None)

            request.session.pop("otp_created",None)

            profile=Profile.objects.get(

                user=user

            )

            if profile.role=="student":

                return redirect(

                    "student_dashboard"

                )

            elif profile.role=="coordinator":

                return redirect(

                    "coordinator_dashboard"

                )

            else:

                return redirect(

                    "employer_dashboard"

                )

        messages.error(

            request,

            "Invalid OTP."

        )

    return render(

        request,

        "otp_verify.html",

        {

            "remaining":remaining

        }

    )
    

def resend_otp_view(request):

    if "otp_user" not in request.session:

        return redirect("login")

    from django.contrib.auth.models import User

    user=User.objects.get(

        id=request.session["otp_user"]

    )

    send_login_otp(

        user,

        request

    )

    messages.success(

        request,

        "A new OTP has been sent."

    )

    return redirect(

        "verify_otp"

    )

    
def home_view(request):

    latest_posts = CommunityPost.objects.filter(
        is_active=True
    ).select_related(
        "author",
        "author__user"
    ).order_by(
        "-created_at"
    )[:3]

    total_students = Profile.objects.filter(
        role="student"
    ).count()

    total_employers = Profile.objects.filter(
        role="employer"
    ).count()

    total_placements = Placement.objects.filter(
        approved=True,
        status="active"
    ).count()

    total_applications = Application.objects.count()

    featured_placements = Placement.objects.filter(
        approved=True,
        status="active"
    ).order_by(
        "-created_at"
    )[:6]

    return render(

        request,

        "home.html",

        {

            "latest_posts": latest_posts,

            "total_students": total_students,

            "total_employers": total_employers,

            "total_placements": total_placements,

            "total_applications": total_applications,

            "featured_placements": featured_placements,

        }

    )
    
@login_required
def student_dashboard_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "student":
        return redirect("home")

    # -----------------------------------------
    # Profile Completion
    # -----------------------------------------

    fields = [
    profile.profile_photo,
    profile.full_name,
    profile.college,
    profile.branch,
    profile.cgpa,
    profile.phone,
    profile.bio,
    profile.skills,
    profile.projects,
    profile.certificates,
    profile.achievements,
    profile.interests,
    profile.github,
    profile.linkedin,
    profile.preferred_role,
    profile.preferred_company,
    profile.preferred_location,
    profile.resume,
]

    completed_fields = 0

    for field in fields:

        if field is None:
            continue

        if isinstance(field, str):

            if field.strip():
                completed_fields += 1

        else:

            completed_fields += 1

        completion_percentage = int(
            (completed_fields / len(fields)) * 100
)

    # -----------------------------------------
    # Dashboard Statistics
    # -----------------------------------------

    applied_count = Application.objects.filter(
        student=profile
    ).count()

    shortlisted_count = Application.objects.filter(
        student=profile,
        status="shortlisted"
    ).count()

    rejected_count = Application.objects.filter(
        student=profile,
        status="rejected"
    ).count()

    selected_count = Application.objects.filter(
        student=profile,
        status="offer_accepted"
    ).count()

    saved_count = SavedPlacement.objects.filter(
        student=profile
    ).count()

    ticket_count = SupportTicket.objects.filter(
        student=profile
    ).count()

    today = date.today()

    upcoming_interview = Interview.objects.filter(

        application__student=profile,

        interview_date__gte=today,

        status="scheduled"

    ).order_by(

        "interview_date",

        "interview_time"

    ).first()

    # -----------------------------------------
    # Community Feed
    # -----------------------------------------

    student_posts = CommunityPost.objects.filter(
        role="student",
        is_active=True
    ).select_related(
        "author",
        "author__user"
    ).order_by("-created_at")[:3]

    coordinator_posts = CommunityPost.objects.filter(
        role="coordinator",
        is_active=True
    ).select_related(
        "author",
        "author__user"
    ).order_by("-created_at")[:3]

    employer_posts = CommunityPost.objects.filter(
        role="employer",
        is_active=True
    ).select_related(
        "author",
        "author__user"
    ).order_by("-created_at")[:3]
    
    print("Completed Fields :", completed_fields)
    print("Total Fields :", len(fields))
    print("Completion :", completion_percentage)

    return render(

        request,

        "student_dashboard.html",

        {

            "applied_count": applied_count,
            "shortlisted_count": shortlisted_count,
            "rejected_count": rejected_count,
            "selected_count": selected_count,
            "saved_count": saved_count,
            "ticket_count": ticket_count,
            "upcoming_interview": upcoming_interview,

            "completion_percentage": completion_percentage,

            "student_posts": student_posts,
            "coordinator_posts": coordinator_posts,
            "employer_posts": employer_posts,

        }

    )
    
    
@login_required
def coordinator_dashboard_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "coordinator":

        return redirect("home")

    student_count = Profile.objects.filter(
        role="student"
    ).count()

    placement_count = Placement.objects.count()

    application_count = Application.objects.count()

    pending_request_count = PlacementRequest.objects.filter(
        department=profile.department,
        status="pending"
    ).count()

    needs_changes_count = PlacementRequest.objects.filter(
        department=profile.department,
        status="needs_changes"
    ).count()

    published_count = PlacementRequest.objects.filter(
        department=profile.department,
        status="published"
    ).count()

    student_posts = CommunityPost.objects.filter(
        role="student",
        is_active=True
    ).select_related(
        "author",
        "author__user"
    ).order_by("-created_at")[:3]

    coordinator_posts = CommunityPost.objects.filter(
        role="coordinator",
        is_active=True
    ).select_related(
        "author",
        "author__user"
    ).order_by("-created_at")[:3]

    employer_posts = CommunityPost.objects.filter(
        role="employer",
        is_active=True
    ).select_related(
        "author",
        "author__user"
    ).order_by("-created_at")[:3]

    return render(

        request,

        "coordinator_dashboard.html",

        {

            "student_count": student_count,

            "placement_count": placement_count,

            "application_count": application_count,

            "pending_request_count": pending_request_count,

            "needs_changes_count": needs_changes_count,

            "published_count": published_count,

            "student_posts": student_posts,

            "coordinator_posts": coordinator_posts,

            "employer_posts": employer_posts,

        }

    )
    
        
    
@login_required
def deactivate_account_view(request):

    profile = Profile.objects.get(

        user=request.user

    )

    if request.method == "POST":

        profile.is_account_active = False

        profile.save()

        logout(request)

        messages.success(

            request,

            "Your account has been temporarily deactivated. Simply log in again anytime to reactivate it."

        )

        return redirect("home")

    return render(

        request,

        "accounts/deactivate_account.html"

    )

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role == "student":

        fields = [

        profile.profile_photo,
        profile.full_name,
        profile.college,
        profile.branch,
        profile.cgpa,
        profile.phone,
        profile.bio,
        profile.skills,
        profile.projects,
        profile.certificates,
        profile.achievements,
        profile.interests,
        profile.github,
        profile.linkedin,
        profile.preferred_role,
        profile.preferred_company,
        profile.preferred_location,
        profile.resume,

    ]

    elif profile.role == "coordinator":

        fields = [

        profile.profile_photo,
        profile.full_name,
        profile.department,
        profile.designation,
        profile.office_email,
        profile.phone,
        profile.bio,

    ]

    elif profile.role == "employer":

        fields = [

        profile.profile_photo,
        profile.full_name,
        profile.company_name,
        profile.company_website,
        profile.company_address,
        profile.company_description,
        profile.hr_designation,
        profile.phone,

    ] 


    completed_fields = sum(
    1 for field in fields if field
)
    
    completion_percentage = round(
    (completed_fields / len(fields)) * 100
)
    

    return render(
    request,
    'profile.html',
    {
        'profile': profile,
        'completion_percentage': completion_percentage,
        'is_own_profile': True,
    }
)
    
@login_required
def student_profile_view(request, profile_id):

    profile = get_object_or_404(
        Profile,
        id=profile_id,
        role="student"
    )

    fields = [
        profile.profile_photo,
        profile.full_name,
        profile.college,
        profile.branch,
        profile.cgpa,
        profile.phone,
        profile.bio,
        profile.skills,
        profile.projects,
        profile.certificates,
        profile.achievements,
        profile.interests,
        profile.github,
        profile.linkedin,
        profile.preferred_role,
        profile.preferred_company,
        profile.preferred_location,
        profile.resume,
    ]

    completed_fields = sum(
        1 for field in fields if field
    )

    completion_percentage = round(
        (completed_fields / len(fields)) * 100
    )

    return render(
    request,
    "profile.html",
    {
        "profile": profile,
        "completion_percentage": completion_percentage,
        "is_own_profile": False,
    }
)   

@login_required
def coordinator_profile_view(request, profile_id):

    profile = get_object_or_404(
        Profile,
        id=profile_id,
        role="coordinator"
    )

    fields = [
        profile.profile_photo,
        profile.full_name,
        profile.department,
        profile.designation,
        profile.experience,
        profile.office_email,
        profile.phone,
        profile.bio,
    ]

    completed_fields = sum(
        1 for field in fields if field
    )

    completion_percentage = round(
        (completed_fields / len(fields)) * 100
    )

    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "completion_percentage": completion_percentage,
            "is_own_profile": False,
        }
    )

@login_required
def edit_profile_view(request):

    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        form = ProfileForm(instance=profile)

    return render(
        request,
        "edit_profile.html",
        {
            "form": form,
            "profile": profile,
        }
    )
    
@login_required
def employer_dashboard_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "employer":

        return redirect("home")

    # -----------------------------------------
    # Placement Request Statistics
    # -----------------------------------------

    request_count = PlacementRequest.objects.filter(
        employer=profile
    ).count()

    pending_requests = PlacementRequest.objects.filter(
        employer=profile,
        status="pending"
    ).count()

    needs_changes_count = PlacementRequest.objects.filter(
        employer=profile,
        status="needs_changes"
    ).count()

    published_count = PlacementRequest.objects.filter(
        employer=profile,
        status="published"
    ).count()

    rejected_count = PlacementRequest.objects.filter(
        employer=profile,
        status="rejected"
    ).count()

    # -----------------------------------------
    # Employer Hiring Statistics
    # -----------------------------------------

    active_placements = Placement.objects.filter(
        employer=profile,
        approved=True,
        status="active",
    ).count()

    total_applicants = Application.objects.filter(
        placement__employer=profile
    ).count()

    shortlisted_count = Application.objects.filter(
        placement__employer=profile,
        status="shortlisted"
    ).count()

    interview_count = Application.objects.filter(
        placement__employer=profile,
        status="interview_scheduled"
    ).count()

    selected_count = Application.objects.filter(
        placement__employer=profile,
        status="offer_accepted"
    ).count()

    # -----------------------------------------
    # Community Feed
    # -----------------------------------------

    student_posts = CommunityPost.objects.filter(
        role="student",
        is_active=True
    ).select_related(
        "author",
        "author__user"
    ).order_by("-created_at")[:3]

    coordinator_posts = CommunityPost.objects.filter(
        role="coordinator",
        is_active=True
    ).select_related(
        "author",
        "author__user"
    ).order_by("-created_at")[:3]

    employer_posts = CommunityPost.objects.filter(
        role="employer",
        is_active=True
    ).select_related(
        "author",
        "author__user"
    ).order_by("-created_at")[:3]

    return render(

        request,

        "employer_dashboard.html",

        {

            "request_count": request_count,

            "pending_requests": pending_requests,

            "needs_changes_count": needs_changes_count,

            "published_count": published_count,

            "rejected_count": rejected_count,

            "active_placements": active_placements,

            "total_applicants": total_applicants,

            "shortlisted_count": shortlisted_count,

            "interview_count": interview_count,

            "selected_count": selected_count,

            "student_posts": student_posts,

            "coordinator_posts": coordinator_posts,

            "employer_posts": employer_posts,

        }

    )


@login_required
def employer_analytics_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "employer":

        return redirect("home")

    placements = Placement.objects.filter(
        employer=profile,
        approved=True,
    )

    applications = Application.objects.filter(
        placement__employer=profile
    )

    total_jobs = placements.count()

    active_jobs = placements.filter(
        status="active"
    ).count()

    closed_jobs = placements.exclude(
        status="closed"
    ).count()

    total_applications = applications.count()

    shortlisted = applications.filter(
        status="shortlisted"
    ).count()

    interviews = applications.filter(
        status="interview_scheduled"
    ).count()

    selected = applications.filter(
        status="offer_accepted"
    ).count()

    rejected = applications.filter(
        status="rejected"
    ).count()

    company_data = (
        applications
        .values("placement__role")
        .annotate(
            total=Count("id")
        )
        .order_by("-total")
    )

    chart_labels = [
        item["placement__role"]
        for item in company_data
    ]

    chart_totals = [
        item["total"]
        for item in company_data
    ]

    recent_applications = (
        applications
        .select_related(
            "student",
            "placement",
        )
        .order_by("-applied_at")[:10]
    )

    return render(

        request,

        "employer_analytics.html",

        {

            "total_jobs": total_jobs,

            "active_jobs": active_jobs,

            "closed_jobs": closed_jobs,

            "total_applications": total_applications,

            "shortlisted": shortlisted,

            "interviews": interviews,

            "selected": selected,

            "rejected": rejected,

            "chart_labels": chart_labels,

            "chart_totals": chart_totals,

            "recent_applications": recent_applications,

        },

    )


@login_required
def coordinator_requests_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "coordinator":

        return redirect("home")

    requests = PlacementRequest.objects.filter(

        department=profile.department,

        status="pending"

    ).order_by(

        "-created_at"

    )

    return render(

        request,

        "placements/coordinator_requests.html",

        {

            "requests": requests

        }

    )