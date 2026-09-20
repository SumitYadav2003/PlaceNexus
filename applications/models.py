from django.db import models

from profiles.models import Profile
from placements.models import Placement


class Application(models.Model):

    STATUS_CHOICES = [

    ("applied", "Applied"),

    ("resume_reviewed", "Resume Reviewed"),

    ("shortlisted", "Shortlisted"),

    ("interview_scheduled", "Interview Scheduled"),

    ("interview_completed", "Interview Completed"),

    ("offer_released", "Offer Released"),

    ("offer_accepted", "Offer Accepted"),

    ("rejected", "Rejected"),
    
    ]

    AVAILABILITY_CHOICES = [
        ('immediately', 'Immediately'),
        ('15_days', 'Within 15 Days'),
        ('30_days', 'Within 30 Days'),
        ('60_days', 'Within 60 Days'),
    ]

    student = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    placement = models.ForeignKey(
        Placement,
        on_delete=models.CASCADE
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    status = models.CharField(
    max_length=30,
    choices=STATUS_CHOICES,
    default="applied"
)

    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='immediately'
    )

    cover_letter = models.TextField(
        blank=True
    )

    def __str__(self):

        return f"{self.student.user.username} - {self.placement.company}"
    
class SavedPlacement(models.Model):

    student = models.ForeignKey(
    Profile,
        on_delete=models.CASCADE
    )

    placement = models.ForeignKey(
        Placement,
        on_delete=models.CASCADE
    )

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            'student',
            'placement'
        )

    def __str__(self):

        return (
            f"{self.student.user.username} "
            f"saved {self.placement.company}"
        )
        
class CompanyReview(models.Model):

    student = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    placement = models.ForeignKey(
        Placement,
        on_delete=models.CASCADE
    )

    rating = models.PositiveSmallIntegerField()

    oa_difficulty = models.PositiveSmallIntegerField()

    interview_difficulty = models.PositiveSmallIntegerField()

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    experience = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "student",
            "placement",
        )

    def __str__(self):

        return (
            f"{self.student.user.username} - "
            f"{self.placement.company}"
        )
        
class SupportTicket(models.Model):

    CATEGORY_CHOICES = [
        ("technical", "Technical Issue"),
        ("placement", "Placement"),
        ("profile", "Profile"),
        ("application", "Application"),
        ("other", "Other"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    student = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    subject = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open"
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"#{self.id} - {self.subject}"

class TicketReply(models.Model):

    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    sender = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"Reply #{self.id} - "
            f"Ticket #{self.ticket.id}"
        )

# -----------------------------------
# Update 28 - Interview Management
# -----------------------------------

class Interview(models.Model):

    MODE_CHOICES = [

        ("online", "Online"),

        ("offline", "Offline"),

    ]

    STATUS_CHOICES = [

        ("scheduled", "Scheduled"),

        ("completed", "Completed"),

        ("cancelled", "Cancelled"),

        ("offer_released", "Offer Released"),

    ]

    application = models.OneToOneField(

        Application,

        on_delete=models.CASCADE

    )

    interview_date = models.DateField()

    interview_time = models.TimeField()

    interview_mode = models.CharField(

        max_length=20,

        choices=MODE_CHOICES

    )

    meeting_link = models.URLField(

        blank=True

    )

    venue = models.CharField(

        max_length=255,

        blank=True

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="scheduled"

    )

    notes = models.TextField(

        blank=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return (

            f"{self.application.student.user.username} - "

            f"{self.application.placement.company}"

        )
        

# -----------------------------
# Referral Opportunity
# -----------------------------

class ReferralOpportunity(models.Model):

    STATUS_CHOICES = [

        ("open", "Open"),

        ("closed", "Closed"),

    ]

    company = models.CharField(
        max_length=150
    )

    role = models.CharField(
        max_length=150
    )

    description = models.TextField()

    coordinator = models.ForeignKey(

        Profile,

        on_delete=models.CASCADE,

        related_name="referrals"

    )

    deadline = models.DateField()

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="open"

    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.company} - {self.role}"
    


# -----------------------------
# Referral Request
# -----------------------------

class ReferralRequest(models.Model):

    STATUS_CHOICES = [

        ("pending", "Pending"),

        ("approved", "Approved"),

        ("rejected", "Rejected"),

    ]

    referral = models.ForeignKey(

        ReferralOpportunity,

        on_delete=models.CASCADE

    )

    student = models.ForeignKey(

        Profile,

        on_delete=models.CASCADE

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="pending"

    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (

            "referral",

            "student",

        )

    def __str__(self):

        return f"{self.student} - {self.referral.company}"
    


# ---------------------------------------
# Update 30 - Community Posts
# ---------------------------------------

class CommunityPost(models.Model):

    ROLE_CHOICES = [

        ("student", "Student"),

        ("coordinator", "Coordinator"),

        ("employer", "Employer"),

    ]

    POST_TYPE_CHOICES = [

        ("achievement", "Achievement"),

        ("interview", "Interview Experience"),

        ("career_question", "Career Question"),

        ("career_tip", "Career Tip"),

        ("placement_drive", "Placement Drive"),

        ("announcement", "Announcement"),

        ("deadline", "Deadline"),

        ("preparation_tip", "Preparation Tip"),

        ("hiring", "Hiring"),

        ("internship", "Internship"),

        ("company_update", "Company Update"),

        ("recruitment_tip", "Recruitment Tip"),

    ]

    author = models.ForeignKey(

        Profile,

        on_delete=models.CASCADE,

        related_name="community_posts"

    )

    role = models.CharField(

        max_length=20,

        choices=ROLE_CHOICES

    )

    post_type = models.CharField(

        max_length=30,

        choices=POST_TYPE_CHOICES

    )

    title = models.CharField(

        max_length=200

    )

    content = models.TextField()

    image = models.ImageField(

        upload_to="community_posts/",

        blank=True,

        null=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    is_active = models.BooleanField(

        default=True

    )

    # NEW
    is_pinned = models.BooleanField(

        default=False

    )

    class Meta:

        ordering = [

            "-is_pinned",

            "-created_at",

        ]

    def __str__(self):

        return f"{self.title} ({self.role})"


# -----------------------------
# Community Like
# -----------------------------

class CommunityLike(models.Model):

    post = models.ForeignKey(

        CommunityPost,

        on_delete=models.CASCADE,

        related_name="likes"

    )

    user = models.ForeignKey(

        Profile,

        on_delete=models.CASCADE

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        unique_together = (

            "post",

            "user",

        )

    def __str__(self):

        return f"{self.user.user.username} likes {self.post.title}"
    
    
    

# -----------------------------
# Community Comment
# -----------------------------

class CommunityComment(models.Model):

    post = models.ForeignKey(

        CommunityPost,

        on_delete=models.CASCADE,

        related_name="comments"

    )

    user = models.ForeignKey(

        Profile,

        on_delete=models.CASCADE

    )

    comment = models.TextField(

        max_length=500

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = [

            "created_at"

        ]

    def __str__(self):

        return (

            f"{self.user.user.username}: "

            f"{self.comment[:25]}"

        )
        


class SavedCommunityPost(models.Model):

    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE
    )

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (

            "user",

            "post",

        )

    def __str__(self):

        return f"{self.user.user.username} saved {self.post.title}"
    
    
    


# =====================================================
# UPDATE 37
# Application Review History
# =====================================================

class ApplicationStatusHistory(models.Model):

    application = models.ForeignKey(

        Application,

        on_delete=models.CASCADE,

        related_name="history"

    )

    updated_by = models.ForeignKey(

        Profile,

        on_delete=models.SET_NULL,

        null=True,

        blank=True

    )

    old_status = models.CharField(

    max_length=30,

    choices=Application.STATUS_CHOICES

)

    new_status = models.CharField(

    max_length=30,

    choices=Application.STATUS_CHOICES

)

    remarks = models.TextField(

        blank=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = [

            "-created_at"

        ]

    def __str__(self):

        return (

            f"{self.application.student.user.username}"

            f" : "

            f"{self.old_status}"

            f" → "

            f"{self.new_status}"

        )
        


# =====================================================
# UPDATE 38
# Notification System
# =====================================================

class Notification(models.Model):

    TYPE_CHOICES = [

        ("application", "Application"),

        ("placement", "Placement"),

        ("interview", "Interview"),

        ("referral", "Referral"),

        ("system", "System"),

    ]

    recipient = models.ForeignKey(

        Profile,

        on_delete=models.CASCADE,

        related_name="notifications"

    )

    title = models.CharField(

        max_length=200

    )

    message = models.TextField()

    notification_type = models.CharField(

        max_length=30,

        choices=TYPE_CHOICES,

        default="system"

    )

    is_read = models.BooleanField(

        default=False

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = [

            "-created_at"

        ]

    def __str__(self):

        return (

            f"{self.recipient.full_name} - "

            f"{self.title}"

        )
        


# =====================================================
# UPDATE 38
# Audit Log
# =====================================================

class AuditLog(models.Model):

    user = models.ForeignKey(

        Profile,

        on_delete=models.SET_NULL,

        null=True,

        blank=True

    )

    action = models.CharField(

        max_length=255

    )

    module = models.CharField(

        max_length=100

    )

    ip_address = models.GenericIPAddressField(

        null=True,

        blank=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = [

            "-created_at"

        ]

    def __str__(self):

        return (

            f"{self.user} - "

            f"{self.action}"

        )