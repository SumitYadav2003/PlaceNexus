from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('coordinator', 'Placement Coordinator'),
        ('employer', 'Employer'),
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
                'autofocus': True,
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
            }
        )
    )

    password1 = forms.CharField(
        help_text=(
            "Password must be at least 8 characters long, "
            "cannot be too common, entirely numeric, "
            "or similar to your username."
        ),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Create password',
                'id': 'password1',
            }
        )
    )

    password2 = forms.CharField(
        help_text="Re-enter your password.",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password',
                'id': 'password2',
            }
        )
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'role'
        ]

    def clean_username(self):

        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():

            raise forms.ValidationError(
                "This username is already taken."
            )

        return username

    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email