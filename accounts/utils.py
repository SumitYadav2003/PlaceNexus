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