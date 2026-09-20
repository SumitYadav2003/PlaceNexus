from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from profiles.models import Profile

from .career_data import career_guides, career_aliases


@login_required
def prepare_view(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "student":
        return render(request, "home.html")

    guide = None

    if request.method == "POST":

        role = request.POST.get("role", "").strip().lower()

        role = career_aliases.get(role, role)

        guide = career_guides.get(role)

        if guide is None:

            guide = {
                "title": "Role Not Found",
                "overview": (
                    "Sorry! We don't have a preparation guide for this role yet. "
                    "Try searching for Software Developer, Data Analyst, "
                    "Backend Developer, Frontend Developer, Cloud Engineer, "
                    "QA Engineer, etc."
                )
            }
    return render(
    request,
    "ai/prepare.html",
    {
        "guide": guide,
        "roles": sorted(career_guides.keys())
    }
)