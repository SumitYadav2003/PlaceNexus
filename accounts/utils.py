from django.conf import settings
from django.core.mail import send_mail
from random import randint
import time
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives

OTP_EXPIRY = 300


def generate_otp():

    return str(randint(100000,999999))


def send_login_otp(user,request):

    otp = generate_otp()

    request.session["otp"] = otp

    request.session["otp_user"] = user.id

    request.session["otp_created"] = int(time.time())

    subject = "PlaceNexus | Login Verification Code"

    html_message = render_to_string(

        "emails/otp_email.html",

    {

            "user": user,

            "otp": otp,

    }

)

    email = EmailMultiAlternatives(

        subject,

        "",

        None,

        [user.email],

)

    email.attach_alternative(

        html_message,

        "text/html"

)

    email.send()


def is_demo_account(user):
    """
    Demo accounts (listed in the DEMO_ACCOUNTS setting) skip the emailed OTP,
    so visitors can try the site without registering.
    Staff and superusers are never treated as demo accounts.
    """

    if user.is_staff or user.is_superuser:
        return False

    return user.username.lower() in settings.DEMO_ACCOUNTS
