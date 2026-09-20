from django.db import models


class Placement(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]

    company = models.CharField(
        max_length=150
    )

    role = models.CharField(
        max_length=150
    )

    package = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    location = models.CharField(
        max_length=150
    )
    
    employer = models.ForeignKey(
        "profiles.Profile",
        on_delete=models.CASCADE,
        null=True,
        blank=True
)
    
    created_by = models.ForeignKey(
    "profiles.Profile",
    related_name="created_placements",
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
    
    approved = models.BooleanField(
        default=False
)
    required_skills = models.TextField(
        blank=True
)
    

    deadline = models.DateField()

    description = models.TextField()
    
    # -----------------------------
# Update 25 - Company Information
# -----------------------------

    company_about = models.TextField(
    blank=True
)

    company_website = models.URLField(
    blank=True
)

    eligibility = models.TextField(
    blank=True,
    help_text="Eligibility Criteria"
)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.company} - {self.role}"
    
    # =====================================================
# UPDATE 32
# Employer Placement Request
# =====================================================

class PlacementRequest(models.Model):

    STATUS_CHOICES = [

        ("pending", "Pending"),

        ("needs_changes", "Needs Changes"),

        ("approved", "Approved"),

        ("rejected", "Rejected"),

        ("published", "Published"),

    ]

    DEPARTMENT_CHOICES = [

        ("Computer Science", "Computer Science"),

        ("Artificial Intelligence", "Artificial Intelligence"),

        ("Data Science", "Data Science"),

        ("Cyber Security", "Cyber Security"),

        ("Information Technology", "Information Technology"),

        ("Electronics", "Electronics"),

        ("Mechanical", "Mechanical"),

        ("Civil", "Civil"),

        ("Electrical", "Electrical"),

        ("Finance", "Finance"),

        ("MBA", "MBA"),

    ]

    employer = models.ForeignKey(

        "profiles.Profile",

        on_delete=models.CASCADE,

        related_name="placement_requests"

    )

    company = models.CharField(

        max_length=200

    )

    role = models.CharField(

        max_length=200

    )

    department = models.CharField(

        max_length=100,

        choices=DEPARTMENT_CHOICES

    )

    package = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    location = models.CharField(

        max_length=200

    )

    openings = models.PositiveIntegerField(

        default=1

    )

    deadline = models.DateField()

    required_skills = models.TextField()

    eligibility = models.TextField()

    description = models.TextField()

    company_about = models.TextField(

        blank=True

    )

    company_website = models.URLField(

        blank=True

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="pending"

    )

    coordinator_comments = models.TextField(

        blank=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )
    def __str__(self):

        return (

        f"{self.company}"

        f" | "

        f"{self.role}"

        f" | "

        f"{self.department}"

        f" | "

        f"{self.status}"

    )




# =====================================================
# UPDATE 34
# Employer ↔ Coordinator Review Workflow
# =====================================================


class PlacementReview(models.Model):

    STATUS_CHOICES = [

        ("under_review", "Under Review"),

        ("needs_changes", "Needs Changes"),

        ("approved", "Approved"),

        ("rejected", "Rejected"),

    ]

    placement_request = models.ForeignKey(

        PlacementRequest,

        on_delete=models.CASCADE,

        related_name="reviews"

    )

    coordinator = models.ForeignKey(

        "profiles.Profile",

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name="placement_reviews"

    )

    status = models.CharField(

        max_length=30,

        choices=STATUS_CHOICES

    )

    comments = models.TextField(

        blank=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return (

            f"{self.placement_request.company}"

            f" - "

            f"{self.status}"

        )


class PlacementRevision(models.Model):

    placement_request = models.ForeignKey(

        PlacementRequest,

        on_delete=models.CASCADE,

        related_name="revisions"

    )

    revision_number = models.PositiveIntegerField()

    edited_by = models.ForeignKey(

        "profiles.Profile",

        on_delete=models.SET_NULL,

        null=True,

        blank=True

    )

    reason = models.TextField(

        blank=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ["-revision_number"]

    def __str__(self):

        return (

            f"{self.placement_request.company}"

            f" Revision "

            f"{self.revision_number}"

        )


class ReviewMessage(models.Model):

    review = models.ForeignKey(

        PlacementReview,

        on_delete=models.CASCADE,

        related_name="messages"

    )

    sender = models.ForeignKey(

        "profiles.Profile",

        on_delete=models.CASCADE

    )

    message = models.TextField()

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ["created_at"]

    def __str__(self):

        return (

            f"Message by "

            f"{self.sender}"

        )
        


# =====================================================
# UPDATE 36
# Employer Public Profile
# =====================================================

class EmployerProfile(models.Model):

    employer = models.OneToOneField(

        "profiles.Profile",

        on_delete=models.CASCADE,

        related_name="employer_profile"

    )

    company_name = models.CharField(

        max_length=200

    )

    company_logo = models.ImageField(

        upload_to="company_logos/",

        blank=True,

        null=True

    )

    company_banner = models.ImageField(

        upload_to="company_banners/",

        blank=True,

        null=True

    )

    industry = models.CharField(

        max_length=150,

        blank=True

    )

    company_size = models.CharField(

        max_length=100,

        blank=True

    )

    founded_year = models.PositiveIntegerField(

        null=True,

        blank=True

    )

    headquarters = models.CharField(

        max_length=200,

        blank=True

    )

    website = models.URLField(

        blank=True

    )

    linkedin = models.URLField(

        blank=True

    )

    description = models.TextField(

        blank=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    def __str__(self):

        return self.company_name

    @property
    def active_jobs(self):

        return Placement.objects.filter(

            employer=self.employer,

            approved=True,

            status="active"

        ).count()

    @property
    def total_jobs(self):

        return Placement.objects.filter(

            employer=self.employer

        ).count()

    @property
    def total_requests(self):

        return PlacementRequest.objects.filter(

            employer=self.employer

        ).count()