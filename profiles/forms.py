from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        role = None

        if self.instance:
            role = self.instance.role

        if role == "student":

            hide_fields = [

            "department",
            "designation",
            "experience",
            "office_email",

            "company_name",
            "company_website",
            "company_address",
            "company_description",
            "hr_designation",

        ]

        elif role == "coordinator":

            hide_fields = [

            "college",
            "branch",
            "cgpa",
            "skills",
            "projects",
            "certificates",
            "achievements",
            "interests",
            "preferred_role",
            "preferred_company",
            "preferred_location",
            "github",
            "linkedin",
            "resume",

            "company_name",
            "company_website",
            "company_address",
            "company_description",
            "hr_designation",

        ]

        elif role == "employer":

            hide_fields = [

            "college",
            "branch",
            "cgpa",
            "skills",
            "projects",
            "certificates",
            "achievements",
            "interests",
            "preferred_role",
            "preferred_company",
            "preferred_location",
            "github",
            "linkedin",
            "resume",

            "department",
            "designation",
            "experience",
            "office_email",

        ]

        else:

            hide_fields = []

        for field in hide_fields:

            self.fields.pop(field, None)

    class Meta:

        model = Profile

        fields = [

    # Common
    'profile_photo',
    'full_name',
    'phone',
    'bio',

    # Student
    'college',
    'branch',
    'cgpa',
    'skills',
    'projects',
    'certificates',
    'achievements',
    'interests',
    'preferred_role',
    'preferred_company',
    'preferred_location',
    'github',
    'linkedin',
    'resume',

    # Coordinator
    'department',
    'designation',
    'experience',
    'office_email',

    # Employer
    'company_name',
    'company_website',
    'company_address',
    'company_description',
    'hr_designation',

        ]

        widgets = {

            'profile_photo': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),

            'full_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'college': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'branch': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'cgpa': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'phone': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),

            'skills': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),

            'projects': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter one project per line'
                }
            ),

            'certificates': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter one certificate per line'
                }
            ),

            'achievements': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter one achievement per line'
                }
            ),

            'interests': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'AI, Cloud Computing, Data Science...'
                }
            ),

            'preferred_role': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'preferred_company': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'preferred_location': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'github': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://github.com/username'
                }
            ),

            'linkedin': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://linkedin.com/in/username'
                }
            ),

            'resume': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),
            
            'department': forms.TextInput(
    attrs={'class': 'form-control'}
),

'designation': forms.TextInput(
    attrs={'class': 'form-control'}
),

'experience': forms.NumberInput(
    attrs={'class': 'form-control'}
),

'office_email': forms.EmailInput(
    attrs={'class': 'form-control'}
),

'company_name': forms.TextInput(
    attrs={'class': 'form-control'}
),

'company_website': forms.URLInput(
    attrs={
        'class': 'form-control',
        'placeholder': 'https://company.com'
    }
),

'company_address': forms.Textarea(
    attrs={
        'class': 'form-control',
        'rows': 3
    }
),

'company_description': forms.Textarea(
    attrs={
        'class': 'form-control',
        'rows': 4
    }
),

'hr_designation': forms.TextInput(
    attrs={'class': 'form-control'}
),

        }