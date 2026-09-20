# PlaceNexus

### Web-Based Placement Management System for Higher Education

PlaceNexus is a full-stack web application designed to centralise and manage university placement activities within a single platform.

The system connects three main stakeholders:

- Students
- Employers
- Placement Coordinators

Instead of handling placements, applications, interviews, candidate management, notifications and administrative tasks through separate systems, PlaceNexus brings these processes together through a secure, role-based workflow.

---

## Table of Contents

- [About the Project](#about-the-project)
- [Project Aim](#project-aim)
- [Main User Roles](#main-user-roles)
- [Key Features](#key-features)
- [Placement Workflow](#placement-workflow)
- [Application Lifecycle](#application-lifecycle)
- [Security and Role-Based Access](#security-and-role-based-access)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Database](#database)
- [Installation and Setup](#installation-and-setup)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Supporting Modules](#supporting-modules)
- [Testing](#testing)
- [Current Limitations](#current-limitations)
- [Future Development](#future-development)
- [Project Status](#project-status)
- [Author](#author)

---

# About the Project

University placement management involves several interconnected activities such as:

- publishing placement opportunities
- reviewing employer submissions
- student applications
- candidate assessment
- recruitment status tracking
- interview scheduling
- communication
- notifications
- reporting
- administrative monitoring

Managing these activities through disconnected systems can make the placement process difficult to monitor and maintain.

**PlaceNexus** addresses this problem by providing a centralised placement-management environment where students, employers and university placement coordinators can interact through clearly defined workflows.

The application is designed specifically around the university placement process rather than acting only as a general job-listing website.

---

# Project Aim

The main aim of PlaceNexus is to design and implement a secure, database-driven web application capable of managing university placement activities for:

- students
- employers
- placement coordinators

through one integrated role-based platform.

The system focuses on the complete placement lifecycle:

```text
Employer creates placement
        ↓
Coordinator reviews placement
        ↓
Placement approved
        ↓
Student discovers placement
        ↓
Student applies
        ↓
Employer reviews candidate
        ↓
Application status progresses
        ↓
Interview scheduled
        ↓
Recruitment outcome recorded
```

---

# Main User Roles

PlaceNexus supports three principal user roles.

## 1. Student

Students can use the system to manage their academic and career information and participate in the placement process.

Student functionality includes:

- Create and manage an account
- Manage student profile
- Maintain academic information
- Add skills
- Upload and manage a resume
- Browse placement opportunities
- Search placements
- Filter placement opportunities
- View placement details
- Save placements
- Remove saved placements
- Apply for placements
- Track submitted applications
- View application status
- View interview information
- Receive system notifications
- Participate in the community
- Access referral opportunities
- Raise support tickets
- Access career-preparation resources

---

## 2. Employer

Employers can manage their organisation and participate directly in the recruitment process.

Employer functionality includes:

- Manage employer/company profile
- Submit placement opportunities
- View submitted placements
- Monitor placement approval status
- Respond to coordinator revision requests
- View applicants for their own placements
- Review candidate information
- Review resumes
- Update recruitment status
- Add review remarks
- Access candidate-management tools
- Schedule interviews
- View placement-related analytics

Employer access is restricted so that an employer can only access candidates associated with placements belonging to that employer.

---

## 3. Placement Coordinator

Placement coordinators provide institutional oversight of the placement process.

Coordinator functionality includes:

- Review employer-submitted placements
- Approve placement opportunities
- Reject placement opportunities
- Request placement changes
- Manage placement information
- Monitor student applications
- Review recruitment activity
- Manage interviews
- Access reports
- Export relevant data
- Review audit information
- Monitor important platform activities

The coordinator role acts as the administrative link between students and employers.

---

# Key Features

## Authentication and Account Management

PlaceNexus provides authentication and account-management functionality for users.

The system separates functionality according to the authenticated user's role.

Protected functionality requires login and users are redirected away from areas they are not authorised to access.

---

## Role-Based Access Control

The application implements role-specific permissions for:

```text
Student
Employer
Coordinator
```

Access restrictions are implemented within the backend rather than relying only on hiding buttons or links in the user interface.

This prevents users from gaining unauthorised access by manually changing URLs.

---

## Student Profiles

Students can maintain academic and professional information such as:

- personal information
- department
- CGPA
- skills
- resume information

Student information is used during placement applications and candidate review.

---

## Placement Discovery

Students can browse placement opportunities and find suitable opportunities using placement-discovery functionality.

Placement information can include:

- company
- role
- location
- package
- application deadline
- placement status
- job/placement description

Students can also save placements for later viewing.

---

## Employer Placement Submission

Employers can create and submit placement opportunities.

Submitted opportunities do not immediately become visible to students.

Instead, they enter a coordinator-controlled review process.

```text
Employer Submission
        ↓
Coordinator Review
        ↓
Approve / Reject / Request Changes
        ↓
Approved Placement
        ↓
Available to Students
```

This provides university oversight of employer-submitted opportunities.

---

## Coordinator Placement Approval

Placement coordinators can review employer submissions and perform actions including:

- Approve
- Reject
- Request changes

Employers can then respond to requested changes before the placement is reviewed again.

This creates a structured placement approval workflow rather than allowing placements to be published directly.

---

## Student Applications

Students can apply for approved placement opportunities.

Each application is connected to:

```text
Student
   ↓
Application
   ↓
Placement
   ↓
Employer
```

Students can then monitor their application and recruitment progress from the platform.

---

# Application Lifecycle

PlaceNexus supports a structured recruitment lifecycle.

An application can progress through stages such as:

```text
Pending
   ↓
Resume Reviewed
   ↓
Shortlisted
   ↓
Interview Scheduled
   ↓
Interview Completed
   ↓
Offer Released
   ↓
Offer Accepted
```

Applications may also move to:

```text
Rejected
```

depending on the recruitment outcome.

---

## Application Status History

PlaceNexus does not store only the current application status.

Important status changes are also retained in application history.

A status-history record can contain:

- previous status
- new status
- user responsible for the change
- remarks
- date and time

For example:

```text
Pending
   ↓
Resume Reviewed
   ↓
Shortlisted
```

The earlier stages are retained rather than being lost when the status changes.

This improves recruitment transparency and traceability.

---

# Employer Candidate Management

PlaceNexus provides an employer candidate-management environment.

Employers can access applications associated with their own placements and review candidate information during the recruitment process.

A key security rule is:

```text
Employer
   ↓
Own Placement
   ↓
Applications for that Placement
   ↓
Candidates
```

An employer cannot access candidates belonging to another employer simply by modifying an application URL or ID.

---

# Interview Management

Authorised users can schedule interviews for placement applications.

Interview information can include details such as:

- interview date
- interview time
- interview mode
- meeting information
- venue information

Interview scheduling is integrated with other system functionality.

For example:

```text
Application
    ↓
Interview Scheduled
    ↓
Interview Record Created
    ↓
Student Notification
    ↓
Email Communication
```

---

# Notifications

PlaceNexus provides an internal notification system for important events.

Notifications allow users to remain informed about activities related to their placement or recruitment process.

Users can manage notification state, including:

- unread notifications
- read notifications
- marking individual notifications as read
- marking notifications as read

---

# Email Communication

Email communication is integrated with relevant system events.

For example, interview scheduling can generate email information containing important interview details for the student.

Sensitive email credentials are stored through environment variables rather than directly inside the source code.

---

# Community

PlaceNexus includes community functionality to support interaction between users.

Community features include functionality such as:

- creating posts
- viewing posts
- interacting with posts
- comments
- likes
- saving posts
- viewing public profiles

This extends PlaceNexus beyond placement applications and provides an additional career-support environment.

---

# Referral System

The platform includes referral functionality where users can interact with referral opportunities.

The system supports:

- referral opportunities
- referral requests
- referral-related user interaction

This provides an additional networking and career-support feature within the same platform.

---

# Support Tickets

Users can create support tickets when they require assistance.

The support system provides a structured method for:

- creating tickets
- viewing submitted tickets
- tracking support requests
- allowing authorised users to access submitted issues

---

# Reporting and Data Export

PlaceNexus provides reporting functionality to support university placement monitoring.

Authorised users can access relevant information about:

- placements
- applications
- recruitment activity
- system activity

Selected information can also be exported for:

- external analysis
- reporting
- administrative record keeping

---

# Audit Logging

Important activities can be recorded through audit information.

Combined with application status history, this allows important system actions to be reviewed later.

This improves:

- transparency
- accountability
- administrative oversight
- recruitment traceability

---

# Security and Role-Based Access

Security is an important part of PlaceNexus because the platform manages information belonging to multiple users and organisations.

The system uses several levels of protection.

## Authentication

Protected functionality requires an authenticated account.

## Role Validation

Users receive functionality according to their assigned role.

```text
Student → Student functionality

Employer → Employer functionality

Coordinator → Coordinator functionality
```

## Resource Ownership Validation

Role checking alone is not sufficient.

For example, even though an employer is allowed to review candidates, the system additionally verifies that the application belongs to one of that employer's placements.

```text
Logged-in Employer
       ↓
Employer Placement
       ↓
Associated Application
       ↓
Candidate Access Granted
```

This prevents one employer from viewing another employer's candidates.

---

# Technology Stack

PlaceNexus was developed using the following technologies.

## Backend

- Python
- Django
- Django ORM

## Database

- PostgreSQL

## Frontend

- HTML5
- CSS3
- Bootstrap
- JavaScript
- Django Templates

## Supporting Technologies

- PostgreSQL database integration
- Django authentication
- Django Forms
- File upload and handling
- Email functionality
- Notifications
- Django Admin
- CSV/data export
- Environment variables using `python-dotenv`

---

# System Architecture

PlaceNexus follows a Django-based web architecture.

A simplified request flow is:

```text
User
 ↓
Browser
 ↓
Django URL Routing
 ↓
Views
 ↓
Forms / Business Logic
 ↓
Django Models
 ↓
Django ORM
 ↓
PostgreSQL Database
```

Templates receive information from the Django backend and display the appropriate interface according to the current user and role.

Supporting services include:

```text
Core Django Application
        │
        ├── Authentication
        ├── Notifications
        ├── Email Communication
        ├── Audit Logging
        ├── Reporting
        ├── Data Export
        └── File Management
```

---

# Project Structure

A simplified structure of the project is shown below:

```text
PlaceNexus/
│
├── accounts/
│   └── Authentication and account-related functionality
│
├── ai_module/
│   └── Career preparation/support functionality
│
├── applications/
│   └── Applications, candidate review and recruitment workflow
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── placements/
│   └── Placement and employer-related functionality
│
├── profiles/
│   └── User and profile management
│
├── static/
│   └── CSS, JavaScript and static resources
│
├── templates/
│   └── Shared Django templates
│
├── manage.py
├── requirements.txt
├── render.yaml
├── .gitignore
└── README.md
```

Local folders such as the following are excluded from Git:

```text
venv/
.env
media/
__pycache__/
```

---

# Database

PlaceNexus uses **PostgreSQL** as its relational database.

The database maintains relationships between entities such as:

```text
User
 ↓
Profile
 ↓
Role
```

Core recruitment relationships include:

```text
Employer
   ↓
Placement
   ↓
Application
   ↓
Student
```

Other relationships include:

```text
Application → Interview

Application → Application Status History

User → Notifications

User → Community Posts

User → Referral Requests

User → Support Tickets

User → Audit Information
```

Django ORM is used to interact with PostgreSQL from the application.

---

# Installation and Setup

The following instructions can be used to run PlaceNexus locally.

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/PlaceNexus.git
```

Move into the project directory:

```bash
cd PlaceNexus
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a file called:

```text
.env
```

inside the project root.

Example:

```env
SECRET_KEY=your_django_secret_key

DB_NAME=placement_db
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_app_password
```

> Never commit the `.env` file to GitHub.

The `.gitignore` file is configured to prevent sensitive environment information from being committed.

---

# PostgreSQL Setup

Ensure PostgreSQL is installed and running.

Create a database called:

```text
placement_db
```

Example using PostgreSQL:

```sql
CREATE DATABASE placement_db;
```

Make sure the database information in your `.env` file matches your PostgreSQL configuration.

---

# Apply Database Migrations

Run:

```bash
python manage.py migrate
```

This will create the database tables required by the Django applications.

---

# Create an Administrator Account

Optional but recommended for local administration:

```bash
python manage.py createsuperuser
```

Enter the requested username, email and password.

The Django administrator interface can then be accessed from the relevant admin URL after starting the application.

---

# Running the Application

Start the Django development server:

```bash
python manage.py runserver
```

The application will normally run at:

```text
http://127.0.0.1:8000/
```

Open the address in a web browser.

---

# Typical Platform Workflow

A complete PlaceNexus placement workflow can be represented as:

```text
Employer Registers
        ↓
Employer Creates Profile
        ↓
Employer Submits Placement
        ↓
Coordinator Reviews Placement
        ↓
Placement Approved
        ↓
Student Browses Placement
        ↓
Student Applies
        ↓
Employer Reviews Candidate
        ↓
Recruitment Status Updated
        ↓
Candidate Shortlisted
        ↓
Interview Scheduled
        ↓
Student Receives Notification
        ↓
Interview Conducted
        ↓
Recruitment Outcome
```

---

# Supporting Modules

PlaceNexus integrates several additional modules alongside the core placement-management functionality.

These include:

- Community
- Referrals
- Support Tickets
- Notifications
- Email Communication
- Reporting
- Data Export
- Audit Logging
- Saved Placements
- Saved Community Posts

The modules operate within the same authenticated user environment rather than functioning as separate applications.

---

# User Interface

The application uses reusable Django templates and consistent user-interface components.

Common interface elements include:

- navigation bars
- dashboards
- cards
- tables
- forms
- search controls
- filters
- buttons
- status badges
- alerts
- notifications
- responsive layouts
- empty-state messages

Different dashboards are provided according to user roles.

```text
Student Dashboard
Employer Dashboard
Coordinator Dashboard
```

---

# Testing

The system was tested across major application workflows, including:

- authentication
- authorisation
- role-based access
- placement submission
- coordinator placement approval
- student applications
- employer candidate access
- application-status transitions
- application status history
- interview scheduling
- notifications
- email communication
- supporting modules
- navigation
- access-control restrictions

Testing was used throughout development to identify and resolve workflow and access-control issues.

---

# Current Limitations

PlaceNexus is an academic web-based prototype and currently has several areas that could be extended further.

Current limitations include:

- No dedicated mobile application
- No large-scale institutional performance testing
- No advanced automated placement-matching system
- No automated candidate-recommendation engine
- Limited formal external user evaluation
- Additional automated testing could be introduced

These limitations provide opportunities for future development.

---

# Future Development

Possible future enhancements include:

- dedicated mobile application
- intelligent placement recommendations
- automated candidate matching
- advanced placement analytics
- expanded automated testing
- large-scale performance testing
- extended employer analytics
- enhanced coordinator reporting
- additional notification preferences
- integration with external university systems
- expanded user evaluation with students, employers and placement staff

---

# Project Status

**Completed academic project / functional prototype**

The implemented system demonstrates an integrated university placement-management environment supporting:

```text
Students
+
Employers
+
Placement Coordinators
```

within a single role-aware Django application.

The main contribution of PlaceNexus is not simply individual placement features, but the integration of the complete placement lifecycle:

```text
Placement Creation
        ↓
Institutional Approval
        ↓
Placement Discovery
        ↓
Student Application
        ↓
Candidate Review
        ↓
Recruitment Tracking
        ↓
Interview Management
        ↓
Notifications
        ↓
Recruitment Outcome
```

alongside supporting community, referral, support, reporting and administrative functionality.

---

# Author

**Sumit Yadav**

MSc Computer Science  
University of Leicester

---

## Academic Project

PlaceNexus was developed as an individual postgraduate computing project focused on the design and implementation of a web-based placement management system for higher education.