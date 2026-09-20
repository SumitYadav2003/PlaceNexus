from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from profiles.models import Profile
from placements.models import Placement
from placements.models import (
    Placement,
    PlacementRequest,
)
from .models import (
    Application,
    SavedPlacement,
    Interview,
    ApplicationStatusHistory,
    Notification,
    AuditLog,
)
from .forms import ApplicationForm
from django.db.models import Count, Max
from django.conf import settings
from django.http import HttpResponseRedirect
from .forms import CompanyReviewForm
from .models import CompanyReview
from .forms import (
    SupportTicketForm,
    TicketReplyForm,
    InterviewForm,
)
from .models import Interview
from .models import (
    SupportTicket,
    TicketReply,
    CommunityPost,
    CommunityLike,
    CommunityComment
)
from django.core.mail import (
    EmailMultiAlternatives,
    send_mail,
)
from django.template.loader import render_to_string
from .models import ReferralOpportunity
from .forms import ReferralOpportunityForm
from .models import (
    ReferralOpportunity,
    ReferralRequest,
)
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import CommunityPost
from .forms import CommunityPostForm
from .models import SavedCommunityPost
from django.shortcuts import get_object_or_404
from django.db.models import Q
import csv
from django.http import HttpResponse



@login_required
def apply_placement_view(request, placement_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != 'student':
        return redirect('home')

    placement = get_object_or_404(
        Placement,
        id=placement_id
    )

    already_applied = Application.objects.filter(
        student=profile,
        placement=placement
    ).exists()

    if already_applied:

        messages.warning(
            request,
            'You have already applied for this placement.'
        )

        return redirect('browse_placements')

    if request.method == "POST":

        form = ApplicationForm(request.POST)

        if form.is_valid():

            application = form.save(commit=False)

            application.student = profile

            application.placement = placement

            application.status = "applied"

            application.save()
            
            Notification.objects.create(

                recipient=profile,

                title="Application Submitted",

                message=(

                    f"You successfully applied for "

                    f"{placement.company} - {placement.role}."

                ),

                notification_type="application",

            )

            AuditLog.objects.create(

    user=profile,

    module="Applications",

    action=f"Applied for {placement.company} - {placement.role}",

    ip_address=request.META.get("REMOTE_ADDR"),

)

            if request.user.email:

                send_mail(
                    subject='Application Submitted',
                    message=(
                        f'Hello {profile.full_name},\n\n'
                        f'Your application for '
                        f'"{placement.company} - {placement.role}" '
                        f'has been submitted successfully.\n\n'
                        f'Current Status: Pending'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=False,
                )

            messages.success(
                request,
                'Application submitted successfully.'
            )

            return redirect('my_applications')

    else:

        form = ApplicationForm()

    return render(
        request,
        'applications/apply_placement.html',
        {
            'form': form,
            'placement': placement,
            'profile': profile,
        }
    )
    
@login_required
def application_list_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != 'coordinator':
        return redirect('home')

    applications = Application.objects.select_related(
        'student',
        'placement'
    ).all().order_by('-applied_at')

    return render(
        request,
        'applications/application_list.html',
        {
            'applications': applications
        }
    )
    
    
@login_required
def employer_candidates_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "employer":

        return redirect("home")

    placements = Placement.objects.filter(

        employer=profile,

        approved=True,

        status="active",

    ).order_by(

        "-created_at"

    )

    applications = Application.objects.filter(

        placement__employer=profile

    ).select_related(

        "student",

        "student__user",

        "placement",

    ).order_by(

        "-applied_at"

    )

    placement_filter = request.GET.get(
        "placement"
    )

    status_filter = request.GET.get(
        "status"
    )

    if placement_filter:

        applications = applications.filter(

            placement_id=placement_filter

        )

    if status_filter:

        applications = applications.filter(

            status=status_filter

        )

    total_candidates = applications.count()

    shortlisted = applications.filter(

        status="shortlisted"

    ).count()

    interviews = applications.filter(

        status="interview_scheduled"

    ).count()

    selected = applications.filter(

        status="offer_accepted"

    ).count()

    return render(

        request,

        "applications/employer_candidates.html",

        {

            "placements": placements,

            "applications": applications,

            "total_candidates": total_candidates,

            "shortlisted": shortlisted,

            "interviews": interviews,

            "selected": selected,

            "placement_filter": placement_filter,

            "status_filter": status_filter,

        },

    )

@login_required
def review_application_view(request, application_id):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role not in [

        "coordinator",

        "employer",

    ]:

        return redirect("home")

    application = get_object_or_404(

        Application,

        id=application_id

    )

    if profile.role == "employer":

        if application.placement.employer != profile:

            return redirect("home")

    history = application.history.all()

    if request.method == "POST":

        status = request.POST.get("status")

        remarks = request.POST.get(
            "remarks",
            ""
        )

        valid_statuses = [

            "applied",

            "resume_reviewed",

            "shortlisted",

            "interview_scheduled",

            "interview_completed",

            "offer_released",

            "offer_accepted",

            "rejected",

        ]

        if status in valid_statuses:

            old_status = application.status

            if old_status != status:

                ApplicationStatusHistory.objects.create(

                    application=application,

                    updated_by=profile,

                    old_status=old_status,

                    new_status=status,

                    remarks=remarks,

                )

                application.status = status

                application.save()
                student_email = application.student.user.email

                if student_email:

                    html_content = render_to_string(

                        "emails/application_status_email.html",

                        {

                            "student_name": application.student.full_name,

                            "company": application.placement.company,

                            "role": application.placement.role,

                            "status": application.get_status_display(),

                            "remarks": remarks,

                        },

                    )

                    email = EmailMultiAlternatives(

                        subject="PlaceNexus | Application Status Updated",

                        body="Application status updated.",

                        from_email=settings.DEFAULT_FROM_EMAIL,

                        to=[student_email],

    )

                    email.attach_alternative(

                        html_content,

                        "text/html",

    )

                    email.send()
                
                Notification.objects.create(

                    recipient=application.student,

                    title="Application Status Updated",

                    message=(

        f"Your application for "

        f"{application.placement.company} "

        f"has been updated to "

        f"{application.get_status_display()}."

    ),

                    notification_type="application",

)

            AuditLog.objects.create(

    user=profile,

    module="Applications",

    action=(

        f"Changed application status "

        f"to {application.status}"

    ),

    ip_address=request.META.get("REMOTE_ADDR"),

)

        if profile.role == "employer":

            return redirect("employer_candidates")

        return redirect("application_list")

    return render(

        request,

        "applications/review_application.html",

        {

            "application": application,

            "history": history,

        },

    )
    
    
@login_required
def my_applications_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "student":
        return redirect("home")

    applications = Application.objects.filter(
        student=profile
    ).select_related(
        "placement"
    ).order_by("-applied_at")

    return render(
        request,
        "applications/my_applications.html",
        {
            "applications": applications
        }
    )

@login_required
def create_ticket_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "student":
        return redirect("home")

    if request.method == "POST":

        form = SupportTicketForm(request.POST)

        if form.is_valid():

            ticket = form.save(commit=False)

            ticket.student = profile

            ticket.save()

            messages.success(
                request,
                "Support ticket created successfully."
            )

            return redirect("my_tickets")

    else:

        form = SupportTicketForm()

    return render(
        request,
        "applications/create_ticket.html",
        {
            "form": form,
        }
    )

@login_required
def add_company_review_view(request, placement_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "student":
        return redirect("home")

    placement = get_object_or_404(
        Placement,
        id=placement_id
    )

    review = CompanyReview.objects.filter(
        student=profile,
        placement=placement
    ).first()

    if request.method == "POST":

        form = CompanyReviewForm(
            request.POST,
            instance=review
        )

        if form.is_valid():

            company_review = form.save(commit=False)

            company_review.student = profile
            company_review.placement = placement

            company_review.save()

            messages.success(
                request,
                "Company review submitted successfully."
            )

            return redirect("company_page", placement.id)

    else:

        form = CompanyReviewForm(
            instance=review
        )

    return render(
        request,
        "applications/company_review.html",
        {
            "form": form,
            "placement": placement,
        }
    )

@login_required
def my_tickets_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "student":
        return redirect("home")

    tickets = SupportTicket.objects.filter(
        student=profile
    ).order_by("-created_at")

    return render(
        request,
        "applications/my_tickets.html",
        {
            "tickets": tickets,
        }
    )
    
@login_required
def ticket_detail_view(request, ticket_id):

    profile = Profile.objects.get(user=request.user)

    ticket = get_object_or_404(
        SupportTicket,
        id=ticket_id
    )

    if profile.role == "student":

        if ticket.student != profile:

            return redirect("home")

    replies = ticket.replies.all().order_by(
        "created_at"
    )
    
    if request.method == "POST" and profile.role == "coordinator":

        new_status = request.POST.get("status")

        if new_status in [
        "open",
        "in_progress",
        "resolved",
        "closed",
    ]:

            ticket.status = new_status
            ticket.save()
        
    if request.method == "POST":

        form = TicketReplyForm(request.POST)

        if form.is_valid():

            reply = form.save(commit=False)

            reply.ticket = ticket

            reply.sender = profile

            reply.save()

            messages.success(
                request,
                "Reply added successfully."
            )

            return redirect(
                "ticket_detail",
                ticket.id
            )

    else:

        form = TicketReplyForm()

    return render(
        request,
        "applications/ticket_detail.html",
        {
            "ticket": ticket,
            "replies": replies,
            "form": form,
        }
    )

@login_required
def support_ticket_list_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    tickets = SupportTicket.objects.all().order_by(
        "-updated_at"
    )

    return render(
        request,
        "applications/support_ticket_list.html",
        {
            "tickets": tickets,
        }
    )
    
        # ==========================================
    # MONTHLY APPLICATIONS
    # ==========================================

    monthly_data = (
        Application.objects
        .annotate(
            month=TruncMonth("applied_at")
        )
        .values("month")
        .annotate(
            total=Count("id")
        )
        .order_by("month")
    )

    monthly_labels = []

    monthly_totals = []

    for row in monthly_data:

        if row["month"]:

            monthly_labels.append(
                row["month"].strftime("%b %Y")
            )

            monthly_totals.append(
                row["total"]
            )

    # ==========================================
    # HIRING FUNNEL
    # ==========================================

    funnel_labels = [

        "Applied",

        "Shortlisted",

        "Interview",

        "Selected",

    ]

    funnel_values = [

        applied_count,

        shortlisted_count,

        interview_count,

        selected_count,

    ]

    # ==========================================
    # SUCCESS RATE
    # ==========================================

    if total_applications > 0:

        success_rate = round(
            (selected_count / total_applications) * 100,
            1,
        )

    else:

        success_rate = 0

    # ==========================================
    # STATUS PIE CHART
    # ==========================================

    status_labels = [

        "Applied",

        "Shortlisted",

        "Interview",

        "Selected",

        "Rejected",

    ]

    status_values = [

        applied_count,

        shortlisted_count,

        interview_count,

        selected_count,

        rejected_count,

    ]

    # ==========================================
    # DASHBOARD CONTEXT
    # ==========================================

    context = {

        "student_count": total_students,

        "students_placed": students_placed,

        "companies_visited": total_companies,

        "highest_package": highest_package,

        "active_placements": active_placements,

        "total_applications": total_applications,

        "recent_applications": recent_applications,

        "companies": companies,

        "totals": totals,

        "top_companies": top_companies,

        "top_roles": top_roles,

        "monthly_labels": monthly_labels,

        "monthly_totals": monthly_totals,

        "status_labels": status_labels,

        "status_values": status_values,

        "funnel_labels": funnel_labels,

        "funnel_values": funnel_values,

        "applied_count": applied_count,

        "shortlisted_count": shortlisted_count,

        "interview_count": interview_count,

        "selected_count": selected_count,

        "rejected_count": rejected_count,

        "success_rate": success_rate,

    }

    return render(

        request,

        "applications/reports_dashboard.html",

        context,

    )

@login_required
def reports_dashboard_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    # ==========================================
    # BASIC COUNTS
    # ==========================================

    total_students = Profile.objects.filter(
        role="student"
    ).count()

    total_companies = Placement.objects.values(
        "company"
    ).distinct().count()

    active_placements = Placement.objects.filter(
        status="active"
    ).count()

    total_applications = Application.objects.count()

    students_placed = Application.objects.filter(
        status="selected"
    ).values("student").distinct().count()

    highest_package = (
        Placement.objects.aggregate(
            Max("package")
        )["package__max"] or 0
    )

    # ==========================================
    # APPLICATION STATUS COUNTS
    # ==========================================

    applied_count = Application.objects.filter(
        status="applied"
    ).count()

    shortlisted_count = Application.objects.filter(
        status="shortlisted"
    ).count()

    interview_count = Application.objects.filter(
        status="interview_scheduled"
    ).count()

    selected_count = Application.objects.filter(
        status="selected"
    ).count()

    rejected_count = Application.objects.filter(
        status="rejected"
    ).count()

    # ==========================================
    # COMPANY BAR CHART
    # ==========================================

    company_report = (
        Application.objects
        .values("placement__company")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    companies = []
    totals = []

    for row in company_report:
        companies.append(row["placement__company"])
        totals.append(row["total"])

    # ==========================================
    # TOP COMPANIES
    # ==========================================

    top_companies = (
        Application.objects
        .values("placement__company")
        .annotate(applications=Count("id"))
        .order_by("-applications")[:5]
    )

    # ==========================================
    # TOP ROLES
    # ==========================================

    top_roles = (
        Application.objects
        .values("placement__role")
        .annotate(applications=Count("id"))
        .order_by("-applications")[:5]
    )

    # ==========================================
    # MONTHLY APPLICATIONS
    # ==========================================

    from django.db.models.functions import TruncMonth

    monthly_data = (
        Application.objects
        .annotate(month=TruncMonth("applied_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    monthly_labels = []
    monthly_totals = []

    for row in monthly_data:

        if row["month"]:

            monthly_labels.append(
                row["month"].strftime("%b %Y")
            )

            monthly_totals.append(
                row["total"]
            )

    # ==========================================
    # RECENT APPLICATIONS
    # ==========================================

    recent_applications = (
        Application.objects
        .select_related(
            "student",
            "placement"
        )
        .order_by("-applied_at")[:10]
    )

    # ==========================================
    # CHARTS
    # ==========================================

    funnel_labels = [
        "Applied",
        "Shortlisted",
        "Interview",
        "Selected",
    ]

    funnel_values = [
        applied_count,
        shortlisted_count,
        interview_count,
        selected_count,
    ]

    status_labels = [
        "Applied",
        "Shortlisted",
        "Interview",
        "Selected",
        "Rejected",
    ]

    status_values = [
        applied_count,
        shortlisted_count,
        interview_count,
        selected_count,
        rejected_count,
    ]

    if total_applications:

        success_rate = round(
            (selected_count / total_applications) * 100,
            1
        )

    else:

        success_rate = 0

    context = {

        "student_count": total_students,
        "students_placed": students_placed,
        "companies_visited": total_companies,
        "highest_package": highest_package,
        "active_placements": active_placements,
        "total_applications": total_applications,

        "companies": companies,
        "totals": totals,

        "top_companies": top_companies,
        "top_roles": top_roles,

        "monthly_labels": monthly_labels,
        "monthly_totals": monthly_totals,

        "status_labels": status_labels,
        "status_values": status_values,

        "funnel_labels": funnel_labels,
        "funnel_values": funnel_values,

        "applied_count": applied_count,
        "shortlisted_count": shortlisted_count,
        "interview_count": interview_count,
        "selected_count": selected_count,
        "rejected_count": rejected_count,

        "success_rate": success_rate,

        "recent_applications": recent_applications,
    }

    return render(
        request,
        "reports/dashboard.html",
        context,
    )
    
@login_required
def save_placement_view(request, placement_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "student":
        return redirect("home")

    placement = get_object_or_404(
        Placement,
        id=placement_id
    )

    SavedPlacement.objects.get_or_create(
        student=profile,
        placement=placement
    )

    messages.success(
    request,
    "Placement saved successfully."
)

    return redirect(
    request.META.get("HTTP_REFERER", "/")
)


@login_required
def saved_placements_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "student":
        return redirect("home")

    saved = SavedPlacement.objects.filter(
        student=profile
    ).select_related(
        "placement"
    ).order_by("-saved_at")
    
    applied_ids = Application.objects.filter(
    student=profile
).values_list(
    "placement_id",
    flat=True
)

    return render(
        request,
        "applications/saved_placements.html",
        {
            "saved": saved,
            "applied_ids": applied_ids,
        }
    )
    
@login_required
def remove_saved_placement_view(request, placement_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "student":
        return redirect("home")

    SavedPlacement.objects.filter(
        student=profile,
        placement_id=placement_id
    ).delete()

    messages.success(
    request,
    "Placement removed from saved list."
)

    return HttpResponseRedirect(
        request.META.get("HTTP_REFERER", "/")
)
    
@login_required
def schedule_interview_view(request, application_id):

    profile = Profile.objects.get(user=request.user)

    # Allow only Employers and Coordinators
    if profile.role not in ["employer", "coordinator"]:
        return redirect("home")

    application = get_object_or_404(
        Application,
        id=application_id
    )

    try:
        interview = Interview.objects.get(
            application=application
        )

    except Interview.DoesNotExist:
        interview = None

    if request.method == "POST":

        form = InterviewForm(
            request.POST,
            instance=interview
        )

        if form.is_valid():

            interview = form.save(commit=False)

            interview.application = application

            interview.save()

            # Update application status
            application.status = "interview_scheduled"
            application.save()

            # Create notification
            Notification.objects.create(
                recipient=application.student,
                title="Interview Scheduled",
                message=(
                    f"Your interview with "
                    f"{application.placement.company} "
                    f"has been scheduled."
                ),
                notification_type="interview",
            )

            # Audit log
            AuditLog.objects.create(
                user=profile,
                module="Interview",
                action=(
                    f"Scheduled interview for "
                    f"{application.student.full_name}"
                ),
                ip_address=request.META.get("REMOTE_ADDR"),
            )

            # Send email
            student_email = application.student.user.email

            if student_email:

                html_content = render_to_string(
                    "emails/interview_email.html",
                    {
                        "student_name": application.student.full_name,
                        "company": application.placement.company,
                        "role": application.placement.role,
                        "interview_date": interview.interview_date.strftime("%d %B %Y"),
                        "interview_time": interview.interview_time.strftime("%I:%M %p"),
                        "interview_mode": interview.get_interview_mode_display(),
                        "meeting_link": interview.meeting_link or "N/A",
                        "venue": interview.venue or "N/A",
                    }
                )

                email = EmailMultiAlternatives(
                    subject="🎓 PlaceNexus | Interview Scheduled",
                    body="Your email client does not support HTML emails.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[student_email],
                )

                email.attach_alternative(
                    html_content,
                    "text/html"
                )

                email.send()

            messages.success(
                request,
                "Interview scheduled and email sent successfully."
            )

            # Redirect according to user role
            if profile.role == "employer":
                return redirect("employer_candidates")
            else:
                return redirect("application_list")

    else:

        form = InterviewForm(
            instance=interview
        )

    return render(
        request,
        "applications/schedule_interview.html",
        {
            "form": form,
            "application": application,
        }
    )
       
    
@login_required
def my_interviews_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "student":
        return redirect("home")

    interviews = Interview.objects.filter(
        application__student=profile
    ).order_by("interview_date", "interview_time")

    return render(
        request,
        "applications/my_interviews.html",
        {
            "interviews": interviews,
        },
    )


@login_required
def create_referral_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "coordinator":
        return redirect("home")

    if request.method == "POST":

        form = ReferralOpportunityForm(
            request.POST
        )

        if form.is_valid():

            referral = form.save(
                commit=False
            )

            referral.coordinator = profile

            referral.save()

            messages.success(

                request,

                "Referral opportunity created successfully."

            )

            return redirect(
                "coordinator_dashboard"
            )

    else:

        form = ReferralOpportunityForm()

    return render(

        request,

        "applications/create_referral.html",

        {

            "form": form

        }

    )
    


@login_required
def referral_list_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    # ==========================
    # STUDENT
    # ==========================

    if profile.role == "student":

        referrals = ReferralOpportunity.objects.filter(
            status="open"
        ).order_by("-created_at")

        referral_requests = ReferralRequest.objects.filter(
            student=profile
        )

        request_map = {}

        for req in referral_requests:

            request_map[req.referral_id] = req.status

        return render(
            request,
            "applications/referral_list.html",
            {
                "referrals": referrals,
                "request_map": request_map,
            },
        )

    # ==========================
    # COORDINATOR
    # ==========================

    elif profile.role == "coordinator":

        referrals = ReferralOpportunity.objects.filter(
            coordinator=profile
        ).order_by("-created_at")

        return render(
            request,
            "applications/my_referrals.html",
            {
                "referrals": referrals,
            },
        )

    return redirect("home")

@login_required
def request_referral_view(request, referral_id):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "student":
        return redirect("home")

    referral = get_object_or_404(
        ReferralOpportunity,
        id=referral_id
    )

    already_requested = ReferralRequest.objects.filter(
        referral=referral,
        student=profile
    ).exists()

    if already_requested:

        messages.warning(
            request,
            "You have already requested this referral."
        )

        return redirect("referral_list")

    ReferralRequest.objects.create(

        referral=referral,

        student=profile,

        status="pending"

    )

    messages.success(

        request,

        "Referral request submitted successfully."

    )

    return redirect("referral_list")



@login_required
def referral_requests_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "coordinator":
        return redirect("home")

    requests = ReferralRequest.objects.select_related(
        "student",
        "referral"
    ).order_by(
        "-requested_at"
    )

    return render(
        request,
        "applications/referral_requests.html",
        {
            "requests": requests,
        }
    )
    

@login_required
def approve_referral_view(request, request_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    referral_request = get_object_or_404(
        ReferralRequest,
        id=request_id
    )

    referral_request.status = "approved"

    referral_request.save()
    
    Notification.objects.create(

    recipient=referral_request.student,

    title="Referral Approved",

    message=(

        f"Your referral request for "

        f"{referral_request.referral.company}"

        f" has been approved."

    ),

    notification_type="referral",

)

    AuditLog.objects.create(

    user=profile,

    module="Referral",

    action="Approved referral request",

    ip_address=request.META.get("REMOTE_ADDR"),

)

    messages.success(
        request,
        "Referral approved successfully."
    )

    return redirect("referral_requests")


@login_required
def reject_referral_view(request, request_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    referral_request = get_object_or_404(
        ReferralRequest,
        id=request_id
    )

    referral_request.status = "rejected"

    referral_request.save()
    
    Notification.objects.create(

    recipient=referral_request.student,

    title="Referral Rejected",

    message=(

        f"Your referral request for "

        f"{referral_request.referral.company}"

        f" was rejected."

    ),

    notification_type="referral",

)

    AuditLog.objects.create(

    user=profile,

    module="Referral",

    action="Rejected referral request",

    ip_address=request.META.get("REMOTE_ADDR"),

)

    messages.success(
        request,
        "Referral rejected successfully."
    )

    return redirect("referral_requests")

@login_required
def community_feed_view(request):

    profile = Profile.objects.select_related("user").get(
        user=request.user
    )

    query = request.GET.get("q", "").strip()

    role = request.GET.get("role", "").strip()

    post_type = request.GET.get("post_type", "").strip()

    posts = (
        CommunityPost.objects
        .filter(is_active=True)
        .select_related(
            "author",
            "author__user"
        )
        .prefetch_related(
            "likes",
            "comments"
        )
    )

    # ================= SEARCH =================

    if query:

        posts = posts.filter(

            Q(title__icontains=query) |

            Q(content__icontains=query) |

            Q(author__full_name__icontains=query) |

            Q(author__user__username__icontains=query) |

            Q(post_type__icontains=query) |

            Q(role__icontains=query)

        )

    # ================= ROLE FILTER =================

    if role:

        posts = posts.filter(
            role=role
        )

    # ================= POST TYPE FILTER =================

    if post_type:

        posts = posts.filter(
            post_type=post_type
        )

    # ================= ORDER =================

    pinned_posts = posts.filter(
        is_pinned=True
    ).order_by("-created_at")

    latest_posts = posts.filter(
        is_pinned=False
    ).order_by("-created_at")

    liked_posts = set(

        CommunityLike.objects.filter(
            user=profile
        ).values_list(
            "post_id",
            flat=True
        )

    )

    saved_posts = set(

        SavedCommunityPost.objects.filter(
            user=profile
        ).values_list(
            "post_id",
            flat=True
        )

    )

    context = {

        "profile": profile,

        "pinned_posts": pinned_posts,

        "latest_posts": latest_posts,

        "liked_posts": liked_posts,

        "saved_posts": saved_posts,

        "student_count": Profile.objects.filter(role="student").count(),

        "coordinator_count": Profile.objects.filter(role="coordinator").count(),

        "employer_count": Profile.objects.filter(role="employer").count(),

        "post_count": CommunityPost.objects.filter(
            is_active=True
        ).count(),

        "query": query,

        "role": role,

        "post_type": post_type,

    }

    return render(

        request,

        "applications/community_feed.html",

        context

    )
    
    
@login_required
def public_profile_view(request, profile_id):

    profile = get_object_or_404(

        Profile,

        id=profile_id

    )

    posts = CommunityPost.objects.filter(

        author=profile,

        is_active=True

    ).order_by(

        "-created_at"

    )

    return render(

        request,

        "applications/public_profile.html",

        {

            "profile_user": profile,

            "posts": posts,

        }

    )

@login_required
def create_post_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    student_choices = [

        ("achievement", "Achievement"),

        ("interview", "Interview Experience"),

        ("career_question", "Career Question"),

        ("career_tip", "Career Tip"),

    ]

    coordinator_choices = [

        ("placement_drive", "Placement Drive"),

        ("announcement", "Announcement"),

        ("deadline", "Deadline"),

        ("preparation_tip", "Preparation Tip"),

    ]

    employer_choices = [

        ("hiring", "Hiring"),

        ("internship", "Internship"),

        ("company_update", "Company Update"),

        ("recruitment_tip", "Recruitment Tip"),

    ]

    if request.method == "POST":

        form = CommunityPostForm(
            request.POST,
            request.FILES
        )

        if profile.role == "student":

            form.fields["post_type"].choices = student_choices

        elif profile.role == "coordinator":

            form.fields["post_type"].choices = coordinator_choices

        elif profile.role == "employer":

            form.fields["post_type"].choices = employer_choices

        if form.is_valid():

            post = form.save(commit=False)

            post.author = profile

            post.role = profile.role

            if profile.role == "coordinator":

                post.is_pinned = (
                    request.POST.get("is_pinned") == "on"
                )

            post.save()

            messages.success(

                request,

                "Community post published successfully."

            )

            return redirect("community_feed")

    else:

        form = CommunityPostForm()

        if profile.role == "student":

            form.fields["post_type"].choices = student_choices

        elif profile.role == "coordinator":

            form.fields["post_type"].choices = coordinator_choices

        elif profile.role == "employer":

            form.fields["post_type"].choices = employer_choices

    return render(

        request,

        "applications/create_post.html",

        {

            "form": form,

            "profile": profile,

        },

    )    
from django.http import JsonResponse


@login_required
def like_post_view(request, post_id):

    profile = Profile.objects.get(
        user=request.user
    )

    post = get_object_or_404(
        CommunityPost,
        id=post_id
    )

    like = CommunityLike.objects.filter(
        post=post,
        user=profile
    )

    if like.exists():

        like.delete()

        liked = False

    else:

        CommunityLike.objects.create(
            post=post,
            user=profile
        )

        liked = True

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        return JsonResponse({

            "liked": liked,

            "likes": post.likes.count(),

            "post_id": post.id,

        })

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "community_feed"
        )
    )
    
@login_required
def add_comment_view(request, post_id):

    if request.method == "POST":

        profile = Profile.objects.get(
            user=request.user
        )

        post = get_object_or_404(
            CommunityPost,
            id=post_id
        )

        comment = request.POST.get(
            "comment",
            ""
        ).strip()

        if comment:

            CommunityComment.objects.create(

                post=post,

                user=profile,

                comment=comment

            )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "community_feed"
        )
    )
@login_required
def save_post(request, post_id):

    profile = Profile.objects.get(
        user=request.user
    )

    post = get_object_or_404(
        CommunityPost,
        id=post_id
    )

    saved_post, created = SavedCommunityPost.objects.get_or_create(

        user=profile,

        post=post

    )

    if created:

        saved = True

    else:

        saved_post.delete()

        saved = False

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        return JsonResponse({

            "saved": saved,

            "post_id": post.id,

        })

    return redirect(

        request.META.get(

            "HTTP_REFERER",

            "community_feed"

        )

    )
    
@login_required
def saved_posts(request):

    profile = Profile.objects.get(
        user=request.user
    )

    saved_posts = SavedCommunityPost.objects.filter(

        user=profile

    ).select_related(

        "post",

        "post__author",

        "post__author__user"

    ).order_by(

        "-saved_at"

    )

    return render(

        request,

        "applications/saved_posts.html",

        {

            "profile": profile,

            "saved_posts": saved_posts,

        }

    )
    


@login_required
def community_post_detail(request, post_id):

    profile = Profile.objects.get(user=request.user)

    post = get_object_or_404(
        CommunityPost,
        id=post_id,
        is_active=True
    )

    liked_posts = CommunityLike.objects.filter(
        user=profile
    ).values_list(
        "post_id",
        flat=True
    )

    saved_posts = SavedCommunityPost.objects.filter(
        user=profile
    ).values_list(
        "post_id",
        flat=True
    )

    related_posts = CommunityPost.objects.filter(
        role=post.role,
        is_active=True
    ).exclude(
        id=post.id
    ).order_by("-created_at")[:3]
    
    comments = CommunityComment.objects.filter(
    post=post
).select_related(
    "user",
    "user__user"
).order_by("created_at")

    return render(
        request,
        "applications/community/post_detail.html",
        {
            "profile": profile,
            "post": post,
            "liked_posts": liked_posts,
            "saved_posts": saved_posts,
            "related_posts": related_posts,
            "comments": comments,
        },
    )
    
    
@login_required
def edit_post_view(request, post_id):

    profile = Profile.objects.get(
        user=request.user
    )

    post = get_object_or_404(
        CommunityPost,
        id=post_id
    )

    if post.author != profile:

        return redirect(
            "community_post_detail",
            post.id
        )

    if request.method == "POST":

        post.title = request.POST.get(
            "title"
        )

        post.content = request.POST.get(
            "content"
        )

        post.post_type = request.POST.get(
            "post_type"
        )

        # Only coordinators can pin posts
        if profile.role == "coordinator":

            post.is_pinned = (
                request.POST.get("is_pinned") == "on"
            )

        # Replace image only if a new one is uploaded
        if request.FILES.get("image"):

            post.image = request.FILES["image"]

        post.save()

        messages.success(

            request,

            "Community post updated successfully."

        )

        return redirect(
            "community_post_detail",
            post.id
        )

    return render(

        request,

        "applications/community/edit_post.html",

        {

            "post": post,

            "profile": profile,

        }

    )

@login_required
def delete_post_view(request, post_id):

    profile = Profile.objects.get(
        user=request.user
    )

    post = get_object_or_404(
        CommunityPost,
        id=post_id
    )

    if post.author != profile:

        return redirect(
            "community_post_detail",
            post.id
        )

    if request.method == "POST":

        post.delete()

        return redirect("community_feed")

    return render(

        request,

        "applications/community/delete_post.html",

        {

            "post": post,

        }

    )



@login_required
def my_posts_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    posts = CommunityPost.objects.filter(
        author=profile,
        is_active=True
    ).select_related(
        "author",
        "author__user"
    ).order_by(
        "-created_at"
    )

    liked_posts = CommunityLike.objects.filter(
        user=profile
    ).values_list(
        "post_id",
        flat=True
    )

    saved_posts = SavedCommunityPost.objects.filter(
        user=profile
    ).values_list(
        "post_id",
        flat=True
    )

    return render(
        request,
        "applications/community/my_posts.html",
        {
            "profile": profile,
            "posts": posts,
            "liked_posts": liked_posts,
            "saved_posts": saved_posts,
        },
    )



@login_required
def community_user_profile(request, profile_id):

    profile = Profile.objects.get(user=request.user)

    viewed_profile = get_object_or_404(
        Profile,
        id=profile_id
    )

    posts = CommunityPost.objects.filter(
        author=viewed_profile,
        is_active=True
    ).order_by("-created_at")

    total_posts = posts.count()

    total_likes = CommunityLike.objects.filter(
        post__author=viewed_profile
    ).count()

    return render(
        request,
        "applications/community/user_profile.html",
        {
            "profile": profile,
            "viewed_profile": viewed_profile,
            "posts": posts,
            "total_posts": total_posts,
            "total_likes": total_likes,
        },
    )



# =====================================================
# UPDATE 38
# Notifications
# =====================================================

@login_required
def notifications_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    notifications = Notification.objects.filter(
        recipient=profile
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "applications/notifications.html",
        {
            "notifications": notifications,
        },
    )


@login_required
def mark_notification_read_view(request, notification_id):

    profile = Profile.objects.get(
        user=request.user
    )

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=profile,
    )

    notification.is_read = True

    notification.save()

    return redirect("notifications")


@login_required
def mark_all_notifications_read_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    Notification.objects.filter(
        recipient=profile,
        is_read=False,
    ).update(
        is_read=True
    )

    return redirect("notifications")


# =====================================================
# UPDATE 38
# Export Reports
# =====================================================

@login_required
def export_applications_report_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "coordinator":

        return redirect("home")

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="applications_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([

        "Student",

        "Company",

        "Role",

        "Status",

        "Applied On",

    ])

    applications = Application.objects.select_related(

        "student",

        "placement",

    ).order_by("-applied_at")

    for application in applications:

        writer.writerow([

            application.student.full_name,

            application.placement.company,

            application.placement.role,

            application.get_status_display(),

            application.applied_at.strftime("%d-%m-%Y"),

        ])

    return response


@login_required
def export_audit_logs_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "coordinator":

        return redirect("home")

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="audit_logs.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([

        "User",

        "Module",

        "Action",

        "IP Address",

        "Created",

    ])

    logs = AuditLog.objects.select_related(
        "user"
    ).order_by("-created_at")

    for log in logs:

        writer.writerow([

            log.user.full_name,

            log.module,

            log.action,

            log.ip_address,

            log.created_at.strftime("%d-%m-%Y %H:%M"),

        ])

    return response






@login_required
def referral_detail_view(request, referral_id):

    referral = get_object_or_404(
        ReferralOpportunity,
        id=referral_id
    )

    return render(
        request,
        "applications/referral_detail.html",
        {
            "referral": referral,
        },
    )