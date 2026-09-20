from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('coordinator', 'Coordinator'),
        ('employer', 'Employer'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    full_name = models.CharField(
        max_length=150,
        blank=True
    )

    college = models.CharField(
        max_length=150,
        blank=True
    )

    branch = models.CharField(
        max_length=100,
        blank=True
    )

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True
    )

    skills = models.TextField(
        blank=True
    )

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    # -----------------------------
    # Update 23 - Student Portfolio
    # -----------------------------

    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    github = models.URLField(
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    projects = models.TextField(
        blank=True,
        help_text="Enter one project per line."
    )

    certificates = models.TextField(
        blank=True,
        help_text="Enter one certificate per line."
    )

    achievements = models.TextField(
        blank=True,
        help_text="Enter one achievement per line."
    )

    interests = models.TextField(
        blank=True,
        help_text="Example: AI, Web Development, Cloud Computing"
    )

    preferred_role = models.CharField(
        max_length=100,
        blank=True
    )

    preferred_company = models.CharField(
        max_length=150,
        blank=True
    )

    preferred_location = models.CharField(
        max_length=100,
        blank=True
    )

# -----------------------------
# Update 25 - Coordinator Profile
# -----------------------------

    department = models.CharField(
        max_length=150,
        blank=True
)

    designation = models.CharField(
        max_length=150,
        blank=True
)

    experience = models.PositiveIntegerField(
    default=0,
        help_text="Years of Experience"
)

    office_email = models.EmailField(
        blank=True
)
    
    # -----------------------------
# Update 29 Enhancement - Employer Profile
# -----------------------------

    company_name = models.CharField(
    max_length=200,
    blank=True
)

    company_website = models.URLField(
    blank=True
)

    company_address = models.TextField(
    blank=True
)

    company_description = models.TextField(
    blank=True
)

    hr_designation = models.CharField(
    max_length=150,
    blank=True
)
    
    # -----------------------------
# Update 31 - Account Status
# -----------------------------

    is_account_active = models.BooleanField(
    default=True
)
    is_permanently_deactivated = models.BooleanField(
    default=False
)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
