from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from profiles.models import Profile


class PublicPagesTests(TestCase):
    """Pages anyone can open without logging in."""

    def test_home_page_loads(self):
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)

    def test_login_page_loads(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)

    def test_register_page_loads(self):
        self.assertEqual(self.client.get(reverse('register')).status_code, 200)


class AccessControlTests(TestCase):
    """Private pages must send anonymous visitors to the login page."""

    def test_student_dashboard_requires_login(self):
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_otp_page_without_login_attempt_redirects_to_login(self):
        response = self.client.get(reverse('verify_otp'))
        self.assertRedirects(response, reverse('login'))


class LoginOtpFlowTests(TestCase):
    """Login -> emailed OTP code -> dashboard."""

    def setUp(self):
        self.password = 'StrongPass!12345'
        self.user = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password=self.password,
        )
        Profile.objects.create(user=self.user, role='student')

    def _login(self, password=None):
        return self.client.post(
            reverse('login'),
            {'username': 'student1', 'password': password or self.password},
        )

    def test_wrong_password_is_rejected_and_sends_no_email(self):
        response = self._login(password='not-the-password')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_valid_login_emails_an_otp_and_redirects_to_verification(self):
        response = self._login()
        self.assertRedirects(response, reverse('verify_otp'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['student1@example.com'])
        html_body = mail.outbox[0].alternatives[0][0]
        self.assertIn(self.client.session['otp'], html_body)

    def test_correct_otp_logs_the_student_in(self):
        self._login()
        otp = self.client.session['otp']
        response = self.client.post(reverse('verify_otp'), {'otp': otp})
        self.assertRedirects(
            response,
            reverse('student_dashboard'),
            fetch_redirect_response=False,
        )
        self.assertEqual(
            int(self.client.session['_auth_user_id']), self.user.id
        )

    def test_wrong_otp_is_rejected(self):
        self._login()
        real_otp = self.client.session['otp']
        wrong_otp = '000000' if real_otp != '000000' else '111111'
        response = self.client.post(reverse('verify_otp'), {'otp': wrong_otp})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)