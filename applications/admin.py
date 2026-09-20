from django.contrib import admin

from .models import (
    Application,
    SavedPlacement,
    CompanyReview,
    SupportTicket,
    TicketReply,
    Interview,
    ReferralOpportunity,
    ReferralRequest,
    CommunityPost,
    ApplicationStatusHistory,
    Notification,
    AuditLog,
)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "placement",
        "status",
        "applied_at",
        "updated_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "student__user__username",
        "placement__company",
        "placement__role",
    )


admin.site.register(SavedPlacement)

admin.site.register(CompanyReview)

admin.site.register(SupportTicket)

admin.site.register(TicketReply)

admin.site.register(Interview)

admin.site.register(ReferralOpportunity)

admin.site.register(ReferralRequest)


@admin.register(ApplicationStatusHistory)
class ApplicationStatusHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "application",
        "old_status",
        "new_status",
        "updated_by",
        "created_at",
    )

    list_filter = (
        "new_status",
    )

    search_fields = (
        "application__student__user__username",
        "application__placement__company",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "recipient",
        "title",
        "notification_type",
        "is_read",
        "created_at",
    )

    list_filter = (
        "notification_type",
        "is_read",
    )

    search_fields = (
        "recipient__user__username",
        "recipient__full_name",
        "title",
        "message",
    )

    ordering = (
        "-created_at",
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "module",
        "action",
        "ip_address",
        "created_at",
    )

    list_filter = (
        "module",
    )

    search_fields = (
        "user__user__username",
        "user__full_name",
        "action",
    )

    ordering = (
        "-created_at",
    )

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author",
        "role",
        "post_type",
        "created_at",
        "is_active",
    )

    list_filter = (
        "role",
        "post_type",
        "is_active",
    )

    search_fields = (
        "title",
        "content",
        "author__full_name",
    )

    ordering = (
        "-created_at",
    )