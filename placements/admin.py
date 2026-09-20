from django.contrib import admin

from .models import (
    Placement,
    PlacementRequest,
    PlacementReview,
    PlacementRevision,
    ReviewMessage,
    EmployerProfile,
)


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "role",
        "package",
        "location",
        "deadline",
        "status",
    )

    list_filter = (
        "status",
        "location",
    )

    search_fields = (
        "company",
        "role",
        "location",
    )


@admin.register(PlacementRequest)
class PlacementRequestAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "role",
        "department",
        "employer",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "department",
    )

    search_fields = (
        "company",
        "role",
        "employer__user__username",
    )


@admin.register(PlacementReview)
class PlacementReviewAdmin(admin.ModelAdmin):

    list_display = (
        "placement_request",
        "coordinator",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "placement_request__company",
    )


@admin.register(PlacementRevision)
class PlacementRevisionAdmin(admin.ModelAdmin):

    list_display = (
        "placement_request",
        "revision_number",
        "edited_by",
        "created_at",
    )

    search_fields = (
        "placement_request__company",
    )


@admin.register(ReviewMessage)
class ReviewMessageAdmin(admin.ModelAdmin):

    list_display = (
        "review",
        "sender",
        "created_at",
    )

    search_fields = (
        "sender__user__username",
        "review__placement_request__company",
    )


# =====================================================
# UPDATE 36
# Employer Public Profile
# =====================================================

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "employer",
        "industry",
        "company_size",
        "headquarters",
        "active_jobs",
        "total_jobs",
    )

    list_filter = (
        "industry",
        "company_size",
    )

    search_fields = (
        "company_name",
        "industry",
        "headquarters",
        "employer__user__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "active_jobs",
        "total_jobs",
        "total_requests",
    )

    fieldsets = (

        (
            "Employer",
            {
                "fields": (
                    "employer",
                )
            },
        ),

        (
            "Company Information",
            {
                "fields": (
                    "company_name",
                    "company_logo",
                    "company_banner",
                    "description",
                )
            },
        ),

        (
            "Business Details",
            {
                "fields": (
                    "industry",
                    "company_size",
                    "founded_year",
                    "headquarters",
                )
            },
        ),

        (
            "Online Presence",
            {
                "fields": (
                    "website",
                    "linkedin",
                )
            },
        ),

        (
            "Statistics",
            {
                "fields": (
                    "active_jobs",
                    "total_jobs",
                    "total_requests",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),

    )