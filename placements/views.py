from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from profiles.models import Profile
from .models import Placement
from .forms import PlacementForm
from django.db.models import Q
from applications.models import (
    Application,
    SavedPlacement
)
from applications.models import CompanyReview
from .forms import EmployerPlacementForm
from profiles.models import Profile
import csv
from django.http import HttpResponse
from .models import (
    PlacementRequest,
    PlacementReview,
    PlacementRevision,
    ReviewMessage,
    EmployerProfile,
)
from .forms import (

    PlacementRequestForm,
    EmployerProfileForm,

)

@login_required
def add_placement_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    if request.method == "POST":

        form = PlacementForm(request.POST)

        if form.is_valid():

            placement = form.save(commit=False)

            placement.created_by = profile

            placement.approved = True

            placement.save()

            messages.success(
                request,
                "Placement added successfully."
            )

            return redirect("placement_list")

    else:

        form = PlacementForm()

    return render(
        request,
        "placements/add_placement.html",
        {
            "form": form
        }
    )
    
@login_required
def placement_list_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    # Only approved placements should be managed here
    placements = Placement.objects.all().order_by(
    "-created_at"
)

    return render(
        request,
        "placements/placement_list.html",
        {
            "placements": placements
        }
    )
    
@login_required
def edit_placement_view(request, placement_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != 'coordinator':
        return redirect('home')

    placement = get_object_or_404(
        Placement,
        id=placement_id
    )

    if request.method == 'POST':

        form = PlacementForm(
            request.POST,
            instance=placement
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Placement updated successfully.'
            )

            return redirect('placement_list')

    else:

        form = PlacementForm(
            instance=placement
        )

    return render(
        request,
        'placements/edit_placement.html',
        {
            'form': form,
            'placement': placement
        }
    )
    
@login_required
def delete_placement_view(request, placement_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    placement = get_object_or_404(
        Placement,
        id=placement_id
    )

    if request.method == "POST":

        placement.status = "archived"
        placement.save()

        messages.success(
            request,
            "Placement archived successfully."
        )

        return redirect("placement_list")

    return render(
        request,
        "placements/delete_placement.html",
        {
            "placement": placement
        }
    )
    
@login_required
def student_placement_list_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != 'student':
        return redirect('home')

    placements = Placement.objects.filter(
    status='active',
    approved=True
).order_by('-created_at')

    search = request.GET.get('search', '').strip()
    location = request.GET.get('location', '').strip()

    if search:

        placements = placements.filter(

            Q(company__icontains=search) |
            Q(role__icontains=search)

        )

    if location:

        placements = placements.filter(
        location__iexact=location
)

    locations = Placement.objects.values_list(
        'location',
        flat=True
    ).distinct()

    applied_ids = Application.objects.filter(
    student=profile
).values_list(
    'placement_id',
    flat=True
)

    saved_ids = SavedPlacement.objects.filter(
    student=profile
).values_list(
    'placement_id',
    flat=True
)
    
    return render(
    request,
    'placements/student_placements.html',
    {
        'placements': placements,
        'locations': locations,
        'search': search,
        'selected_location': location,
        'applied_ids': applied_ids,
        'saved_ids': saved_ids,
    }
)

@login_required
def company_page_view(request, placement_id):

    placement = get_object_or_404(
        Placement,
        id=placement_id
    )

    company_placements = Placement.objects.filter(
    company=placement.company,
    status="active",
    approved=True
).order_by("-created_at")
    
    profile = Profile.objects.get(
    user=request.user
)

    applied_ids = []

    if profile.role == "student":

        applied_ids = Application.objects.filter(
        student=profile
    ).values_list(
        "placement_id",
        flat=True
    )
    
    saved_ids = []

    if profile.role == "student":

        saved_ids = SavedPlacement.objects.filter(
        student=profile
    ).values_list(
        "placement_id",
        flat=True
    )
    
    reviews = CompanyReview.objects.filter(
    placement__company=placement.company
).order_by("-created_at")

    return render(
        request,
        "placements/company_page.html",
        {
            "placement": placement,
            "company_placements": company_placements,
            "applied_ids": applied_ids,
            "saved_ids": saved_ids,
            "reviews": reviews,
        }
    )
    
@login_required
def restore_placement_view(request, placement_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    placement = get_object_or_404(
        Placement,
        id=placement_id
    )

    placement.status = "active"
    placement.save()

    messages.success(
        request,
        "Placement restored successfully."
    )

    return redirect("placement_list")



@login_required
def employer_submit_placement_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "employer":
        return redirect("home")

    if request.method == "POST":

        form = EmployerPlacementForm(request.POST)

        if form.is_valid():

            placement = form.save(commit=False)

            placement.created_by = profile

            placement.employer = profile

            placement.approved = False

            placement.save()

            messages.success(

                request,

                "Placement submitted successfully and is awaiting coordinator approval."

            )

            return redirect("employer_dashboard")

    else:

        form = EmployerPlacementForm()

    return render(

        request,

        "placements/employer_submit_placement.html",

        {

            "form": form

        }

    )



@login_required
def employer_placements_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "employer":
        return redirect("home")

    placements = Placement.objects.filter(
        employer=profile
    ).order_by("-created_at")

    return render(
        request,
        "placements/employer_placements.html",
        {
            "placements": placements
        }
    )

@login_required
def employer_pending_placements_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    placements = Placement.objects.filter(
        employer__isnull=False,
        approved=False
    ).order_by("-created_at")

    return render(
        request,
        "placements/employer_pending_placements.html",
        {
            "placements": placements
        }
    )
    
@login_required
def approve_employer_placement_view(request, placement_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    placement = get_object_or_404(
        Placement,
        id=placement_id
    )

    placement.approved = True

    placement.status = "active"

    placement.save()

    messages.success(
        request,
        "Employer placement approved successfully."
    )

    return redirect("employer_pending_placements")

@login_required
def export_placements_csv_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="placements.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
writer.writerow([
    "Company",
    "Role",
    "Department",
    "Package (£k / Per Annum)",
    "Location",
    "Deadline",
    "Status",
    "Approved",
    "Employer",
    "Published On",
])
    ])

    placements = Placement.objects.order_by(
    "-created_at"
)

    for placement in placements:

        writer.writerow([
    placement.company,
    placement.role,
    getattr(placement, "department", "-"),
    placement.package,
    placement.location,
    placement.deadline,
    placement.status.title(),
    "Yes" if placement.approved else "No",
    placement.employer.full_name if placement.employer else "-",
    placement.created_at.strftime("%d-%m-%Y"),
        ])

    return response


@login_required
def export_applications_csv_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="applications.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
    "Student",
    "Department",
    "Company",
    "Role",
    "Application Status",
    "Applied On",
    ])

    applications = Application.objects.select_related(
    "student",
    "placement",
).order_by(
    "-applied_at"
)

    for application in applications:

        writer.writerow([
    application.student.full_name,
    application.student.department,
    application.placement.company,
    application.placement.role,
    application.get_status_display(),
    application.applied_at.strftime("%d-%m-%Y %H:%M"),
        ])

    return response



# =====================================================
# UPDATE 32
# Employer Placement Request
# =====================================================

@login_required
def create_request_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "employer":

        return redirect("home")

    if request.method == "POST":

        form = PlacementRequestForm(
            request.POST
        )

        if form.is_valid():

            placement_request = form.save(
                commit=False
            )

            placement_request.employer = profile
            
            placement_request.status = "pending"

            placement_request.coordinator_comments = ""

            placement_request.save()

            messages.success(

                request,

                "Your placement request has been submitted successfully. It is now awaiting coordinator approval."

            )

            return redirect(
                "my_requests"
            )

    else:

        form = PlacementRequestForm()

    return render(

        request,

        "placements/create_request.html",

        {

            "form": form

        }

    )


@login_required
def my_requests_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "employer":

        return redirect("home")

    requests = PlacementRequest.objects.filter(

        employer=profile

    ).order_by(

        "-created_at"

    )

    return render(

        request,

        "placements/my_requests.html",

        {

            "requests": requests

        }

    )
    


# =====================================================
# UPDATE 32
# Coordinator Review Workflow
# =====================================================
@login_required
def review_request_view(request, request_id):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "coordinator":
        return redirect("home")

    placement_request = get_object_or_404(
        PlacementRequest,
        id=request_id
    )

    reviews = PlacementReview.objects.filter(
    placement_request=placement_request
    ).select_related(
    "coordinator"
    ).order_by("-created_at")

    revisions = PlacementRevision.objects.filter(
    placement_request=placement_request
    ).select_related(
    "edited_by"
)

    activity_history = []

    activity_history.append(
    {
        "type": "submitted",
        "title": "Placement Request Submitted",
        "description": (
            "Employer submitted this placement request."
        ),
        "time": placement_request.created_at,
    }
)

    for review in reviews:

        if review.status == "approved":

            title = "Coordinator Approved"

        elif review.status == "needs_changes":

            title = "Coordinator Requested Changes"

        elif review.status == "rejected":

            title = "Coordinator Rejected Request"

        else:

            title = "Coordinator Reviewed"

        activity_history.append(
        {
            "type": "review",
            "title": title,
            "description": review.comments,
            "time": review.created_at,
            "review": review,
        }
    )

    for revision in revisions:

        activity_history.append(
        {
            "type": "revision",
            "title": (
                f"Employer Resubmitted "
                f"(Revision {revision.revision_number})"
            ),
            "description": revision.reason,
            "time": revision.created_at,
            "revision": revision,
        }
    )

    activity_history = sorted(
    activity_history,
    key=lambda x: x["time"],
    reverse=True
)

    if placement_request.department != profile.department:

        messages.error(
            request,
            "You are not authorised to review this request."
        )

        return redirect("coordinator_requests")

    if request.method == "POST":

        action = request.POST.get("action")

        placement_request.coordinator_comments = request.POST.get(
            "comments"
        )

        review = PlacementReview.objects.create(

            placement_request=placement_request,

            coordinator=profile,

            status="under_review",

            comments=placement_request.coordinator_comments,

        )

        if action == "needs_changes":

            placement_request.status = "needs_changes"

            review.status = "needs_changes"

            review.save()

            messages.success(
                request,
                "Revision request sent to employer."
            )

        elif action == "approve":

            if Placement.objects.filter(

                employer=placement_request.employer,

                company=placement_request.company,

                role=placement_request.role,

                approved=True,

                status="active",

            ).exists():

                messages.warning(
                    request,
                    "This placement is already published."
                )

                return redirect("coordinator_requests")

            Placement.objects.create(

                company=placement_request.company,

                role=placement_request.role,

                package=placement_request.package,

                location=placement_request.location,

                deadline=placement_request.deadline,

                description=placement_request.description,

                required_skills=placement_request.required_skills,

                company_about=placement_request.company_about,

                company_website=placement_request.company_website,

                eligibility=placement_request.eligibility,

                employer=placement_request.employer,

                created_by=profile,

                approved=True,

                status="active",

            )

            placement_request.status = "published"

            review.status = "approved"

            review.save()

            messages.success(
                request,
                "Placement published successfully."
            )

        elif action == "reject":

            placement_request.status = "rejected"

            review.status = "rejected"

            review.save()

            messages.success(
                request,
                "Placement request rejected."
            )

        placement_request.save()

        return redirect("coordinator_requests")

    return render(

    request,

    "placements/review_request.html",

    {

        "request_obj": placement_request,

        "reviews": reviews,

        "revisions": revisions,

        "activity_history": activity_history,

    }

)

@login_required
def approve_request_view(request, request_id):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "coordinator":
        return redirect("home")

    placement_request = get_object_or_404(
        PlacementRequest,
        id=request_id
    )

    if placement_request.department != profile.department:

        messages.error(
            request,
            "You cannot approve requests outside your department."
        )

        return redirect("coordinator_requests")

    if Placement.objects.filter(

        employer=placement_request.employer,
        company=placement_request.company,
        role=placement_request.role,
        approved=True,
        status="active",

    ).exists():

        messages.warning(
            request,
            "This placement has already been published."
        )

        return redirect("coordinator_requests")

    Placement.objects.create(

        company=placement_request.company,

        role=placement_request.role,

        package=placement_request.package,

        location=placement_request.location,

        deadline=placement_request.deadline,

        description=placement_request.description,

        required_skills=placement_request.required_skills,

        company_about=placement_request.company_about,

        company_website=placement_request.company_website,

        eligibility=placement_request.eligibility,

        employer=placement_request.employer,

        created_by=profile,

        approved=True,

        status="active",

    )

    placement_request.status = "published"

    placement_request.coordinator_comments = (
        "Approved and published."
    )

    placement_request.save()

    messages.success(
        request,
        "Placement published successfully."
    )

    return redirect("coordinator_requests")


@login_required
def reject_request_view(request, request_id):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "coordinator":

        return redirect("home")

    placement_request = get_object_or_404(

        PlacementRequest,

        id=request_id

    )

    placement_request.status = "rejected"

    if request.method == "POST":

        placement_request.coordinator_comments = request.POST.get(

            "comments",

            ""

    )

    placement_request.save()

    messages.success(

        request,

        "Placement request rejected."

    )

    return redirect(

        "coordinator_requests"

    )
    

@login_required
def edit_request_view(request, request_id):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "employer":
        return redirect("home")

    placement_request = get_object_or_404(

        PlacementRequest,

        id=request_id,

        employer=profile

    )

    if placement_request.status != "needs_changes":

        messages.error(

            request,

            "Only requests marked 'Needs Changes' can be edited."

        )

        return redirect(

            "my_requests"

        )

    if request.method == "POST":

        form = PlacementRequestForm(

            request.POST,

            instance=placement_request

        )

        if form.is_valid():

            request_obj = form.save(commit=False)

            request_obj.status = "pending"

            request_obj.coordinator_comments = ""
            
            latest_revision = PlacementRevision.objects.filter(

                placement_request=request_obj

            ).count()

            PlacementRevision.objects.create(

            placement_request=request_obj,

    revision_number=latest_revision + 1,

    edited_by=profile,

    reason="Employer updated placement after coordinator review."

)

            request_obj.save()

            messages.success(

                request,

                "Placement request resubmitted successfully."

            )

            return redirect(

                "my_requests"

            )

    else:

        form = PlacementRequestForm(

            instance=placement_request

        )

    return render(

        request,

        "placements/create_request.html",

        {

            "form": form,

            "editing": True

        }

    )
    

@login_required
def permanent_delete_placement_view(request, placement_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "coordinator":
        return redirect("home")

    placement = get_object_or_404(
        Placement,
        id=placement_id
    )

    if request.method == "POST":

        placement.delete()

        messages.success(
            request,
            "Placement permanently deleted."
        )

        return redirect("placement_list")

    return render(
        request,
        "placements/permanent_delete_placement.html",
        {
            "placement": placement
        }
    )
    



# =====================================================
# UPDATE 36
# Employer Public Profile
# =====================================================

@login_required
def edit_employer_profile_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != "employer":

        return redirect("home")

    employer_profile, created = EmployerProfile.objects.get_or_create(

        employer=profile,

        defaults={

            "company_name": profile.full_name or "Company"

        }

    )

    if request.method == "POST":

        form = EmployerProfileForm(

            request.POST,

            request.FILES,

            instance=employer_profile

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Company profile updated successfully."

            )

            return redirect(
                "edit_employer_profile"
            )

    else:

        form = EmployerProfileForm(
            instance=employer_profile
        )

    return render(

        request,

        "placements/edit_employer_profile.html",

        {

            "form": form,

            "profile": employer_profile,

        }

    )


@login_required
def public_employer_profile_view(request, profile_id):

    employer = get_object_or_404(

        Profile,

        id=profile_id,

        role="employer"

    )

    employer_profile = get_object_or_404(

        EmployerProfile,

        employer=employer

    )

    active_jobs = Placement.objects.filter(

        employer=employer,

        approved=True,

        status="active"

    ).order_by(

        "-created_at"

    )

    return render(

        request,

        "placements/public_employer_profile.html",

        {

            "employer": employer,

            "company": employer_profile,

            "active_jobs": active_jobs,

        }

    )