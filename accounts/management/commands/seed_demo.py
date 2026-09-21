"""
Create (or reset) the public demo accounts and their sample data.

Usage (PowerShell, from the project folder):
    $env:DEMO_PASSWORD = "choose-a-demo-password"
    python manage.py seed_demo

Running it again deletes the three demo accounts (and everything they own:
placements, applications, posts) and rebuilds them, so it also works as a
"reset the demo" button.

Everything created here is invented sample data. The demo accounts have no
email address, so the app never tries to send them email.
"""

import os
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from applications.models import (
    Application,
    CommunityPost,
    ReferralOpportunity,
    SavedPlacement,
)
from placements.models import EmployerProfile, Placement
from profiles.models import Profile

DEMO_STUDENT = 'demo_student'
DEMO_COORDINATOR = 'demo_coordinator'
DEMO_EMPLOYER = 'demo_employer'
DEMO_USERNAMES = [DEMO_STUDENT, DEMO_COORDINATOR, DEMO_EMPLOYER]

COMPANY_ABOUT = 'Invented company used for PlaceNexus demo data.'
COMPANY_SITE = 'https://example.com'


class Command(BaseCommand):
    help = 'Create or reset the demo accounts (student, coordinator, employer) with sample data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            help='Password for the demo accounts (or set the DEMO_PASSWORD environment variable).',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        password = options.get('password') or os.getenv('DEMO_PASSWORD')

        if not password:
            raise CommandError(
                'No password given. Set DEMO_PASSWORD or pass --password.'
            )

        if len(password) < 8:
            raise CommandError('The demo password must be at least 8 characters.')

        # Reset: deleting the users also deletes their profiles, placements,
        # applications and posts.
        User.objects.filter(username__in=DEMO_USERNAMES).delete()

        today = date.today()

        # ---------------- Accounts ----------------
        student_user = User.objects.create_user(
            username=DEMO_STUDENT, password=password,
            first_name='Demo', last_name='Student',
        )
        coordinator_user = User.objects.create_user(
            username=DEMO_COORDINATOR, password=password,
            first_name='Demo', last_name='Coordinator',
        )
        employer_user = User.objects.create_user(
            username=DEMO_EMPLOYER, password=password,
            first_name='Demo', last_name='Employer',
        )

        student = Profile.objects.create(
            user=student_user,
            role='student',
            full_name='Demo Student',
            college='Sample University',
            branch='Computer Science',
            cgpa=Decimal('8.20'),
            skills='Python, Django, SQL, PostgreSQL, JavaScript, REST APIs',
            bio='Sample student profile for exploring PlaceNexus.',
            projects='Campus placement portal\nRecipe recommendation app',
            interests='Web development, Data engineering',
            preferred_role='Software Engineer',
            preferred_location='Leicester',
        )
        coordinator = Profile.objects.create(
            user=coordinator_user,
            role='coordinator',
            full_name='Demo Coordinator',
            department='Careers and Placements',
            designation='Placement Coordinator',
            experience=5,
        )
        employer = Profile.objects.create(
            user=employer_user,
            role='employer',
            full_name='Demo Employer',
        )
        EmployerProfile.objects.create(
            employer=employer,
            company_name='Fernleaf Software',
            industry='Software',
            company_size='50-200 employees',
            founded_year=2014,
            headquarters='Leicester, UK',
            website=COMPANY_SITE,
            description='Invented software company used for PlaceNexus demo data.',
        )

        # ---------------- Placements ----------------
        def make_placement(owner_field, owner, company, role, package, location, days, skills, description):
            return Placement.objects.create(
                company=company,
                role=role,
                package=Decimal(package),
                location=location,
                approved=True,
                status='active',
                deadline=today + timedelta(days=days),
                required_skills=skills,
                description=description,
                company_about=COMPANY_ABOUT,
                company_website=COMPANY_SITE,
                eligibility='Final-year or recently graduated students with a relevant degree.',
                created_by=owner,
                **({'employer': owner} if owner_field == 'employer' else {}),
            )

        p1 = make_placement(
            'employer', employer, 'Fernleaf Software', 'Junior Python Developer',
            '32.00', 'Leicester (Hybrid)', 21,
            'Python, Django, SQL, Git',
            'Build and maintain web features for our customer portal with a small friendly team.',
        )
        p2 = make_placement(
            'employer', employer, 'Fernleaf Software', 'Graduate Data Engineer',
            '34.00', 'Leicester (Hybrid)', 35,
            'Python, SQL, PostgreSQL, ETL',
            'Help design and run data pipelines that feed our analytics dashboards.',
        )
        p3 = make_placement(
            'coordinator', coordinator, 'Kestrel Data Labs', 'Data Analyst',
            '30.00', 'London', 28,
            'SQL, Excel, Power BI, Python',
            'Turn client data into clear reports and dashboards.',
        )
        p4 = make_placement(
            'coordinator', coordinator, 'Lumen Cloudworks', 'Cloud Support Engineer',
            '29.00', 'Manchester', 14,
            'Linux, Networking, AWS, Troubleshooting',
            'First-line cloud support with a structured training programme.',
        )
        p5 = make_placement(
            'coordinator', coordinator, 'Harbor and Pine Analytics', 'Junior Full-Stack Developer',
            '31.00', 'Birmingham (Remote-friendly)', 42,
            'JavaScript, HTML, CSS, Python, REST APIs',
            'Work across the front end and back end of our reporting tools.',
        )
        p6 = make_placement(
            'coordinator', coordinator, 'Orbitline Systems', 'Software Tester (QA)',
            '27.00', 'London (Hybrid)', 30,
            'Testing, Selenium, SQL, Bug tracking',
            'Plan and run tests for new releases of our logistics software.',
        )

        # ---------------- Student activity ----------------
        Application.objects.create(
            student=student, placement=p1, status='interview_scheduled',
            availability='immediately',
            cover_letter='Sample cover letter: I enjoy building Django applications.',
        )
        Application.objects.create(
            student=student, placement=p3, status='shortlisted',
            availability='15_days',
            cover_letter='Sample cover letter: I like turning data into insight.',
        )
        Application.objects.create(
            student=student, placement=p6, status='applied',
            availability='30_days',
            cover_letter='Sample cover letter: I care about software quality.',
        )
        SavedPlacement.objects.create(student=student, placement=p2)
        SavedPlacement.objects.create(student=student, placement=p5)

        # ---------------- Community and referrals ----------------
        CommunityPost.objects.create(
            author=coordinator, role='coordinator', post_type='announcement',
            title='Welcome to the PlaceNexus demo',
            content='This is sample data. Explore the placements, applications and community feed.',
            is_pinned=True,
        )
        CommunityPost.objects.create(
            author=employer, role='employer', post_type='hiring',
            title='Fernleaf Software is hiring graduates',
            content='We have openings for a junior Python developer and a graduate data engineer.',
        )
        CommunityPost.objects.create(
            author=student, role='student', post_type='preparation_tip',
            title='How I prepare for technical interviews',
            content='Practise explaining your projects out loud, and revise SQL joins.',
        )
        ReferralOpportunity.objects.create(
            company='Kestrel Data Labs', role='Data Analyst',
            description='Sample referral opportunity posted by the placement coordinator.',
            coordinator=coordinator, deadline=today + timedelta(days=20),
        )

        if options.get('verbosity', 1) > 0:
            self.stdout.write(self.style.SUCCESS('Demo accounts and sample data created.'))
            self.stdout.write(f"Usernames: {', '.join(DEMO_USERNAMES)}")
            self.stdout.write(
                'To let them skip the emailed OTP, set this environment variable on Render:\n'
                f"  DEMO_ACCOUNTS={','.join(DEMO_USERNAMES)}"
            )
