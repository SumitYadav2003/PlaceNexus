import os
from unittest import mock

from django.contrib.auth.models import User
from django.core import mail
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse

from profiles.models import Profile

DEMO_PASSWORD = 'demo-password-123'
DEMO_ACCOUNTS = ['demo_student', 'demo_coordinator', 'demo_employer']


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


@override_settings(DEMO_ACCOUNTS=DEMO_ACCOUNTS)
class DemoAccountTests(TestCase):
    """Demo accounts skip the OTP; everyone else still needs it."""

    @classmethod
    def setUpTestData(cls):
        call_command('seed_demo', password=DEMO_PASSWORD, verbosity=0)

    def _login(self, username, password=DEMO_PASSWORD):
        return self.client.post(
            reverse('login'), {'username': username, 'password': password}
        )

    def test_demo_student_skips_otp_and_reaches_dashboard(self):
        response = self._login('demo_student')
        self.assertRedirects(response, reverse('student_dashboard'))
        self.assertEqual(len(mail.outbox), 0)

    def test_demo_coordinator_skips_otp_and_reaches_dashboard(self):
        response = self._login('demo_coordinator')
        self.assertRedirects(response, reverse('coordinator_dashboard'))

    def test_demo_employer_skips_otp_and_reaches_dashboard(self):
        response = self._login('demo_employer')
        self.assertRedirects(response, reverse('employer_dashboard'))

    def test_demo_student_can_open_the_main_pages(self):
        self._login('demo_student')
        for name in ('browse_placements', 'my_applications',
                     'saved_placements', 'community_feed', 'profile'):
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_demo_login_with_wrong_password_is_rejected(self):
        response = self._login('demo_student', password='wrong-password')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_regular_users_still_need_the_otp(self):
        user = User.objects.create_user(
            username='real_student', email='real@example.com', password='StrongPass!12345'
        )
        Profile.objects.create(user=user, role='student')
        response = self._login('real_student', password='StrongPass!12345')
        self.assertRedirects(response, reverse('verify_otp'))
        self.assertEqual(len(mail.outbox), 1)

    def test_staff_accounts_never_skip_the_otp(self):
        admin = User.objects.create_superuser(
            username='demo_student_admin', email='admin@example.com', password='StrongPass!12345'
        )
        Profile.objects.create(user=admin, role='coordinator')
        with override_settings(DEMO_ACCOUNTS=DEMO_ACCOUNTS + ['demo_student_admin']):
            response = self._login('demo_student_admin', password='StrongPass!12345')
        self.assertRedirects(response, reverse('verify_otp'))

    def test_demo_accounts_cannot_be_permanently_deactivated(self):
        self._login('demo_student')
        self.client.post(reverse('permanent_deactivate_account'))
        profile = Profile.objects.get(user__username='demo_student')
        self.assertFalse(profile.is_permanently_deactivated)
        self.assertTrue(profile.is_account_active)


class DemoModeOffTests(TestCase):
    """With DEMO_ACCOUNTS empty (the default) nobody skips the OTP."""

    @override_settings(DEMO_ACCOUNTS=[])
    def test_seeded_demo_user_still_needs_the_otp_when_the_feature_is_off(self):
        user = User.objects.create_user(username='demo_student', password=DEMO_PASSWORD, email='d@example.com')
        Profile.objects.create(user=user, role='student')
        response = self.client.post(
            reverse('login'), {'username': 'demo_student', 'password': DEMO_PASSWORD}
        )
        self.assertRedirects(response, reverse('verify_otp'))


class SeedDemoCommandTests(TestCase):
    def test_requires_a_password(self):
        with mock.patch.dict(os.environ):
            os.environ.pop('DEMO_PASSWORD', None)
            with self.assertRaises(CommandError):
                call_command('seed_demo', verbosity=0)

    def test_rejects_a_short_password(self):
        with self.assertRaises(CommandError):
            call_command('seed_demo', password='short', verbosity=0)

    def test_can_be_run_twice_without_duplicates(self):
        call_command('seed_demo', password=DEMO_PASSWORD, verbosity=0)
        call_command('seed_demo', password=DEMO_PASSWORD, verbosity=0)
        self.assertEqual(User.objects.filter(username__in=DEMO_ACCOUNTS).count(), 3)
        self.assertEqual(Profile.objects.filter(user__username__in=DEMO_ACCOUNTS).count(), 3)

    def test_demo_accounts_have_no_email_so_the_app_never_emails_them(self):
        call_command('seed_demo', password=DEMO_PASSWORD, verbosity=0)
        for user in User.objects.filter(username__in=DEMO_ACCOUNTS):
            self.assertEqual(user.email, '')
