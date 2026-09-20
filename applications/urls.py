from django.urls import path
import csv
from django.http import HttpResponse
from . import views

urlpatterns = [

    path(
        "apply/<int:placement_id>/",
        views.apply_placement_view,
        name="apply_placement",
    ),

    path(
        "applications/",
        views.application_list_view,
        name="application_list",
    ),

    path(
        "review-application/<int:application_id>/",
        views.review_application_view,
        name="review_application",
    ),

    path(
        "my-applications/",
        views.my_applications_view,
        name="my_applications",
    ),

    # ==========================================
    # Employer Candidate Dashboard
    # ==========================================

    path(
        "employer-candidates/",
        views.employer_candidates_view,
        name="employer_candidates",
    ),

    path(
        "reports/",
        views.reports_dashboard_view,
        name="reports_dashboard",
    ),

    path(
        "save-placement/<int:placement_id>/",
        views.save_placement_view,
        name="save_placement",
    ),

    path(
        "saved-placements/",
        views.saved_placements_view,
        name="saved_placements",
    ),

    path(
        "remove-saved-placement/<int:placement_id>/",
        views.remove_saved_placement_view,
        name="remove_saved_placement",
    ),

    path(
        "company-review/<int:placement_id>/",
        views.add_company_review_view,
        name="company_review",
    ),

    path(
        "create-ticket/",
        views.create_ticket_view,
        name="create_ticket",
    ),

    path(
        "my-tickets/",
        views.my_tickets_view,
        name="my_tickets",
    ),

    path(
        "ticket/<int:ticket_id>/",
        views.ticket_detail_view,
        name="ticket_detail",
    ),

    path(
        "support-tickets/",
        views.support_ticket_list_view,
        name="support_ticket_list",
    ),

    path(
        "schedule-interview/<int:application_id>/",
        views.schedule_interview_view,
        name="schedule_interview",
    ),

    path(
        "my-interviews/",
        views.my_interviews_view,
        name="my_interviews",
    ),

    path(
        "create-referral/",
        views.create_referral_view,
        name="create_referral",
    ),

    path(
        "referrals/",
        views.referral_list_view,
        name="referral_list",
    ),

    path(
        "request-referral/<int:referral_id>/",
        views.request_referral_view,
        name="request_referral",
    ),

    path(
        "referral-requests/",
        views.referral_requests_view,
        name="referral_requests",
    ),

    path(
        "approve-referral/<int:request_id>/",
        views.approve_referral_view,
        name="approve_referral",
    ),

    path(
        "reject-referral/<int:request_id>/",
        views.reject_referral_view,
        name="reject_referral",
    ),

    path(
        "community/",
        views.community_feed_view,
        name="community_feed",
    ),

    path(
        "community/create/",
        views.create_post_view,
        name="create_post",
    ),

    path(
        "community/like/<int:post_id>/",
        views.like_post_view,
        name="like_post",
    ),

    path(
        "community/comment/<int:post_id>/",
        views.add_comment_view,
        name="add_comment",
    ),

    path(
        "profile/<int:profile_id>/",
        views.public_profile_view,
        name="public_profile",
    ),

    path(
        "community/save/<int:post_id>/",
        views.save_post,
        name="save_post",
    ),

    path(
        "community/saved/",
        views.saved_posts,
        name="saved_posts",
    ),

    path(
        "community/post/<int:post_id>/",
        views.community_post_detail,
        name="community_post_detail",
    ),

    path(
        "community/post/<int:post_id>/edit/",
        views.edit_post_view,
        name="edit_post",
    ),

    path(
        "community/post/<int:post_id>/delete/",
        views.delete_post_view,
        name="delete_post",
    ),

    path(
        "community/my-posts/",
        views.my_posts_view,
        name="my_posts",
    ),

    path(
        "community/profile/<int:profile_id>/",
        views.community_user_profile,
        name="community_user_profile",
    ),
    
    # =====================================================
# UPDATE 38
# Notifications
# =====================================================

path(
    "notifications/",
    views.notifications_view,
    name="notifications",
),

path(
    "notifications/read/<int:notification_id>/",
    views.mark_notification_read_view,
    name="mark_notification_read",
),

path(
    "notifications/read-all/",
    views.mark_all_notifications_read_view,
    name="mark_all_notifications_read",
),
path(
    "reports/export-applications/",
    views.export_applications_report_view,
    name="export_applications_report",
),

path(
    "reports/export-audit-logs/",
    views.export_audit_logs_view,
    name="export_audit_logs",
),
path(
    "referral/<int:referral_id>/",
    views.referral_detail_view,
    name="referral_detail",
),

]