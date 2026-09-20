from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'role',
        'college',
        'branch',
        'cgpa',
        'phone'
    )

    search_fields = (
        'user__username',
        'full_name',
        'college',
        'branch'
    )

    list_filter = (
        'role',
        'branch'
    )