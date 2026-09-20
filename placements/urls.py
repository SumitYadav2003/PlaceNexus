from django.urls import path
from . import views
from .views import (
    add_placement_view,
    placement_list_view,
    edit_placement_view,
    delete_placement_view,
    permanent_delete_placement_view,
    student_placement_list_view,
    company_page_view,
    restore_placement_view,
    edit_employer_profile_view,
    public_employer_profile_view,
)

urlpatterns = [

    path(
        "add-placement/",
        add_placement_view,
        name="add_placement",
    ),

    path(
        "placements/",
        placement_list_view,
        name="placement_list",
    ),

    path(
        "edit-placement/<int:placement_id>/",
        edit_placement_view,
        name="edit_placement",
    ),

    path(
        "delete-placement/<int:placement_id>/",
        delete_placement_view,
        name="delete_placement",
    ),

    path(
        "browse-placements/",
        student_placement_list_view,
        name="browse_placements",
    ),

    path(
        "company/<int:placement_id>/",
        company_page_view,
        name="company_page",
    ),

    path(
        "restore-placement/<int:placement_id>/",
        restore_placement_view,
        name="restore_placement",
    ),
    
    path(
    "employer-submit-placement/",
    views.employer_submit_placement_view,
    name="employer_submit_placement",
),
    path(
    "my-placements/",
    views.employer_placements_view,
    name="employer_placements",
),
    path(
    "pending-employer-placements/",
    views.employer_pending_placements_view,
    name="employer_pending_placements",
),

    path(
    "approve-placement/<int:placement_id>/",
    views.approve_employer_placement_view,
    name="approve_employer_placement",
),
    path(
    "export-placements/",
    views.export_placements_csv_view,
    name="export_placements_csv",
),

path(
    "export-applications/",
    views.export_applications_csv_view,
    name="export_applications_csv",
),

path(

    "placement-request/create/",

    views.create_request_view,

    name="create_request",

),

path(

    "placement-request/my-requests/",

    views.my_requests_view,

    name="my_requests",

),
path(

    "placement-request/<int:request_id>/",

    views.review_request_view,

    name="review_request",

),

path(

    "placement-request/<int:request_id>/approve/",

    views.approve_request_view,

    name="approve_request",

),

path(

    "placement-request/<int:request_id>/reject/",

    views.reject_request_view,

    name="reject_request",

),
path(

    "edit-request/<int:request_id>/",

    views.edit_request_view,

    name="edit_request",

),
path(
    "permanent-delete-placement/<int:placement_id>/",
    permanent_delete_placement_view,
    name="permanent_delete_placement",
),
path(
    "employer-profile/edit/",
    edit_employer_profile_view,
    name="edit_employer_profile",
),

path(
    "employer-profile/<int:profile_id>/",
    public_employer_profile_view,
    name="public_employer_profile",
),
]