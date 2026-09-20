from django import forms

from .models import Application
from .models import CompanyReview
from .models import SupportTicket

from .models import (
    SupportTicket,
    TicketReply,
    Interview,
)
class ApplicationForm(forms.ModelForm):

    class Meta:

        model = Application

        fields = [
            'cover_letter',
            'availability',
        ]

        widgets = {

            'cover_letter': forms.Textarea(

                attrs={
                    'class': 'form-control',
                    'rows': 8,
                    'placeholder':
                    'Write a professional cover letter explaining why you are a suitable candidate for this position.'
                }

            ),

            'availability': forms.Select(

                attrs={
                    'class': 'form-select'
                }

            ),

        }

        labels = {

            'cover_letter': 'Cover Letter',

            'availability': 'Availability',

        }

        help_texts = {

            'cover_letter':
            'Describe your skills, experience and interest in this role.',

        }
        
class CompanyReviewForm(forms.ModelForm):

    class Meta:

        model = CompanyReview

        fields = [
            "rating",
            "oa_difficulty",
            "interview_difficulty",
            "salary",
            "experience",
        ]

        widgets = {

            "rating": forms.Select(
                choices=[
                    (1, "⭐ 1"),
                    (2, "⭐⭐ 2"),
                    (3, "⭐⭐⭐ 3"),
                    (4, "⭐⭐⭐⭐ 4"),
                    (5, "⭐⭐⭐⭐⭐ 5"),
                ],
                attrs={
                    "class": "form-select"
                }
            ),

            "oa_difficulty": forms.Select(
                choices=[
                    (1, "Very Easy"),
                    (2, "Easy"),
                    (3, "Medium"),
                    (4, "Hard"),
                    (5, "Very Hard"),
                ],
                attrs={
                    "class": "form-select"
                }
            ),

            "interview_difficulty": forms.Select(
                choices=[
                    (1, "Very Easy"),
                    (2, "Easy"),
                    (3, "Medium"),
                    (4, "Hard"),
                    (5, "Very Hard"),
                ],
                attrs={
                    "class": "form-select"
                }
            ),

            "salary": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "experience": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Share your interview and hiring experience..."
                }
            ),
        }
        
class SupportTicketForm(forms.ModelForm):

    class Meta:

        model = SupportTicket

        fields = [
            "subject",
            "category",
            "priority",
            "message",
        ]

        widgets = {

            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter ticket subject"
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
            "message": forms.Textarea(
    attrs={
        "class": "form-control",
        "rows": 6,
        "placeholder": "Describe your issue in detail..."
    }
),

        }

class TicketReplyForm(forms.ModelForm):

    class Meta:

        model = TicketReply

        fields = [
            "message"
        ]

        widgets = {

            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Write your reply..."
                }
            )

        }

# -----------------------------------
# Update 28 - Interview Form
# -----------------------------------

class InterviewForm(forms.ModelForm):

    class Meta:

        model = Interview

        fields = [

            "interview_date",

            "interview_time",

            "interview_mode",

            "meeting_link",

            "venue",

            "status",

            "notes",

        ]

        widgets = {

            "interview_date": forms.DateInput(

                attrs={

                    "class": "form-control",

                    "type": "date"

                }

            ),

            "interview_time": forms.TimeInput(

                attrs={

                    "class": "form-control",

                    "type": "time"

                }

            ),

            "interview_mode": forms.Select(

                attrs={

                    "class": "form-select"

                }

            ),

            "meeting_link": forms.URLInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "https://meet.google.com/..."

                }

            ),

            "venue": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Company Office / College Campus"

                }

            ),

            "status": forms.Select(

                attrs={

                    "class": "form-select"

                }

            ),

            "notes": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 5,

                    "placeholder": "Additional interview instructions..."

                }

            ),

        }
        

from .models import (
    ReferralOpportunity,
    ReferralRequest,
)


class ReferralOpportunityForm(forms.ModelForm):

    class Meta:

        model = ReferralOpportunity

        fields = [

            "company",

            "role",

            "description",

            "deadline",

            "status",

        ]

        widgets = {

            "company": forms.TextInput(attrs={
                "class":"form-control form-control-lg rounded-3"
            }),

            "role": forms.TextInput(attrs={
                "class":"form-control form-control-lg rounded-3"
            }),

            "description": forms.Textarea(attrs={
                "class":"form-control rounded-3",
                "rows":5
            }),

            "deadline": forms.DateInput(attrs={
                "class":"form-control form-control-lg rounded-3",
                "type":"date"
            }),

            "status": forms.Select(attrs={
                "class":"form-select form-select-lg rounded-3"
            }),

        }
        


from .models import CommunityPost


class CommunityPostForm(forms.ModelForm):

    class Meta:

        model = CommunityPost

        fields = [

            "post_type",

            "title",

            "content",

            "image",

        ]

        widgets = {

            "post_type": forms.Select(

                attrs={

                    "class": "form-select"

                }

            ),

            "title": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Enter post title"

                }

            ),

            "content": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 6,

                    "placeholder": "Write your post..."

                }

            ),

            "image": forms.ClearableFileInput(

                attrs={

                    "class": "form-control"

                }

            ),

        }