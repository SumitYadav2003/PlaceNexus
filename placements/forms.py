from django import forms
from .models import Placement
from .models import (
    Placement,
    EmployerProfile,
)
from .models import (
    PlacementRequest,
    ReviewMessage,
)

class PlacementForm(forms.ModelForm):

    class Meta:

        model = Placement

        fields = [
    'company',
    'role',
    'package',
    'location',
    'deadline',
    'description',

    # Update 25
    'company_about',
    'company_website',
    'eligibility',

    'status',
        ]

        widgets = {

            'company': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'role': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'package': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'deadline': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5
                }
            ),
            
            'company_about': forms.Textarea(
    attrs={
        'class': 'form-control',
        'rows': 4
    }
),

'company_website': forms.URLInput(
    attrs={
        'class': 'form-control'
    }
),

'eligibility': forms.Textarea(
    attrs={
        'class': 'form-control',
        'rows': 3
    }
),

            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

        }


class EmployerPlacementForm(forms.ModelForm):

    class Meta:

        model = Placement

        fields = [

            "company",

            "role",

            "package",

            "location",

            "deadline",

            "required_skills",

            "description",

            "company_about",

            "company_website",

            "eligibility",

        ]

        widgets = {

            "company": forms.TextInput(attrs={
                "class": "form-control form-control-lg rounded-3",
                "placeholder": "e.g. Google"
            }),

            "role": forms.TextInput(attrs={
                "class": "form-control form-control-lg rounded-3",
                "placeholder": "e.g. Software Engineer"
            }),

            "package": forms.NumberInput(attrs={
                "class": "form-control form-control-lg rounded-3",
                "placeholder": "e.g. 12.5"
            }),

            "location": forms.TextInput(attrs={
                "class": "form-control form-control-lg rounded-3",
                "placeholder": "e.g. Mumbai"
            }),

            "deadline": forms.DateInput(attrs={
                "class": "form-control form-control-lg rounded-3",
                "type": "date"
            }),

            "required_skills": forms.Textarea(attrs={
                "class": "form-control rounded-3",
                "rows": 3,
                "placeholder": "Python, Django, SQL, React..."
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control rounded-3",
                "rows": 5,
                "placeholder": "Describe the job role..."
            }),

            "company_about": forms.Textarea(attrs={
                "class": "form-control rounded-3",
                "rows": 4,
                "placeholder": "Tell students about your company..."
            }),

            "company_website": forms.URLInput(attrs={
                "class": "form-control form-control-lg rounded-3",
                "placeholder": "https://company.com"
            }),

            "eligibility": forms.Textarea(attrs={
                "class": "form-control rounded-3",
                "rows": 3,
                "placeholder": "CGPA, Branches, Graduation Year..."
            }),

        }
        

# =====================================================
# UPDATE 32
# Placement Request Form
# =====================================================

from .models import PlacementRequest


class PlacementRequestForm(forms.ModelForm):

    class Meta:

        model = PlacementRequest

        exclude = [

            "employer",

            "status",

            "coordinator_comments",

            "created_at",

            "updated_at",

        ]

        widgets = {

            "company": forms.TextInput(

                attrs={

                    "class":"form-control form-control-lg",

                    "placeholder":"Google"

                }

            ),

            "role": forms.TextInput(

                attrs={

                    "class":"form-control form-control-lg",

                    "placeholder":"Software Engineer"

                }

            ),

            "department": forms.Select(

                attrs={

                    "class":"form-select form-select-lg"

                }

            ),

            "package": forms.NumberInput(

                attrs={

                    "class":"form-control form-control-lg"

                }

            ),

            "location": forms.TextInput(

                attrs={

                    "class":"form-control form-control-lg"

                }

            ),

            "openings": forms.NumberInput(

                attrs={

                    "class":"form-control form-control-lg"

                }

            ),

            "deadline": forms.DateInput(

                attrs={

                    "class":"form-control",

                    "type":"date"

                }

            ),

            "required_skills": forms.Textarea(

                attrs={

                    "class":"form-control",

                    "rows":3

                }

            ),

            "eligibility": forms.Textarea(

                attrs={

                    "class":"form-control",

                    "rows":3

                }

            ),

            "description": forms.Textarea(

                attrs={

                    "class":"form-control",

                    "rows":5

                }

            ),

            "company_about": forms.Textarea(

                attrs={

                    "class":"form-control",

                    "rows":4

                }

            ),

            "company_website": forms.URLInput(

                attrs={

                    "class":"form-control"

                }

            ),

        }
        
    
# =====================================================
# UPDATE 34
# Review Conversation Form
# =====================================================

from .models import ReviewMessage


class ReviewMessageForm(forms.ModelForm):

    class Meta:

        model = ReviewMessage

        fields = [

            "message",

        ]

        widgets = {

            "message": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 3,

                    "placeholder": "Write a reply..."

                }

            )

        }

        labels = {

            "message": ""

        }
        


# =====================================================
# UPDATE 36
# Employer Public Profile Form
# =====================================================

class EmployerProfileForm(forms.ModelForm):

    class Meta:

        model = EmployerProfile

        fields = [

            "company_name",

            "company_logo",

            "company_banner",

            "industry",

            "company_size",

            "founded_year",

            "headquarters",

            "website",

            "linkedin",

            "description",

        ]

        widgets = {

            "company_name": forms.TextInput(

                attrs={

                    "class":"form-control form-control-lg",

                    "placeholder":"Company Name"

                }

            ),

            "industry": forms.TextInput(

                attrs={

                    "class":"form-control",

                    "placeholder":"Software, Finance, Healthcare..."

                }

            ),

            "company_size": forms.TextInput(

                attrs={

                    "class":"form-control",

                    "placeholder":"100-500 Employees"

                }

            ),

            "founded_year": forms.NumberInput(

                attrs={

                    "class":"form-control",

                    "placeholder":"2018"

                }

            ),

            "headquarters": forms.TextInput(

                attrs={

                    "class":"form-control",

                    "placeholder":"Mumbai"

                }

            ),

            "website": forms.URLInput(

                attrs={

                    "class":"form-control",

                    "placeholder":"https://company.com"

                }

            ),

            "linkedin": forms.URLInput(

                attrs={

                    "class":"form-control",

                    "placeholder":"https://linkedin.com/company/..."

                }

            ),

            "description": forms.Textarea(

                attrs={

                    "class":"form-control",

                    "rows":6,

                    "placeholder":"Tell students about your company..."

                }

            ),

            "company_logo": forms.ClearableFileInput(

                attrs={

                    "class":"form-control"

                }

            ),

            "company_banner": forms.ClearableFileInput(

                attrs={

                    "class":"form-control"

                }

            ),

        }