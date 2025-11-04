<p align="center">
  <a href="https://generalassemb.ly/">
    <img src="https://github.com/user-attachments/assets/0284af1b-bf15-408c-b724-98868f976667" alt="General Assembly" height="80"/>
  <a href="https://sda.edu.sa/">
  </a><img width="500" height="80" alt="Sda-logo-color" src="https://github.com/user-attachments/assets/5edb2838-4fe6-4b18-b80d-706b31f56a64" />
</p>

# GoldenCare Backend API
### Frontend Repository    [GoldenCare Frontend](https://github.com/RaghadAlbeladi1/GoldenCare-frontend/tree/main)
### Backend Link [GoldenCare](http://127.0.0.1:8000/)

## Project Description

GoldenCare is a comprehensive platform connecting families and caregivers to provide home-based senior care. The platform enables families to book caregiver services, manage appointments, access electronic health records (EHR), and write reviews. This backend API serves as the core of the GoldenCare ecosystem, providing RESTful endpoints for authentication, appointment management, health records, and service coordination.

## Repository Description

This repository contains the Django REST Framework backend for GoldenCare, a senior care management platform. The API provides secure authentication using JWT tokens, manages appointments with flexible duration options, handles electronic health records, and facilitates caregiver-service matching.

## Tech Stack

- **Framework**: Django 5.2.7
- **API**: Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL
- **Python**: 3.12
- **Dependencies**:
  - psycopg2-binary (PostgreSQL adapter)
  - django-cors-headers (CORS handling)
  - python-dateutil (Date utilities)

## Installation Instructions

### Using Docker (Recommended)

1. **Prerequisites**:
   - Docker Desktop installed and running
   - Docker Compose installed (included with Docker Desktop)

2. **Clone the repository**:
   ```bash
   git clone https://github.com/RaghadAlbeladi1/GoldenCare-backend.git
   cd GoldenCare-backend
   ```

3. **Navigate to project root** (where docker-compose.yml is located):
   ```bash
   cd ../capstone-project
   ```

4. **Create environment file** (if not exists):
   ```bash
   # Create .env.dev file in backend directory with your configuration
   # Example:
   # SECRET_KEY=your-secret-key
   # DEBUG=True
   # DATABASE_URL=postgresql://docker_django_user:hello_django@db:5432/GoldenCaredb
   ```

5. **Build and run containers**:
   ```bash
   docker-compose up --build
   ```

6. **Access the application**:
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/api/`

7. **View logs**:
   ```bash
   docker-compose logs -f api
   ```

8. **Stop containers**:
   ```bash
   docker-compose down
   ```

9. **Stop and remove volumes** (clean database):
   ```bash
   docker-compose down -v
   ```

### Manual Installation (Without Docker)

1. **Prerequisites**:
   - Python 3.12 or higher
   - PostgreSQL 16 or higher
   - pip (Python package manager)

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**:
   - Create a PostgreSQL database named `GoldenCaredb`
   - Update database settings in `settings.py` or use environment variables

5. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Backend API: `http://localhost:8000`

## RESTful Routing Table

<details open>

##  Authentication

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `POST` | `/auth/register` | create | Register a new user (patient) |
| `POST` | `/auth/login` | create | User login (returns token) |
| `POST` | `/auth/logout` | destroy | User logout |

## Users (Patients)

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `GET` | `/users/profile` | show | Get current user profile |
| `PUT` | `/users/profile` | update | Update user profile |
| `PATCH` | `/users/profile` | update | Partially update user profile |
| `DELETE` | `/users/profile` | destroy | Delete user account |


##  Caregivers

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `GET` | `/caregivers` | index | List all caregivers |
| `GET` | `/caregivers/:id` | show | Show caregiver details (including service) |


## Services

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `GET` | `/services` | index | List all active services |
| `GET` | `/services/:id` | show | Show service details (including caregiver info) |
| `GET` | `/services/search` | index | Search services by name or specialization |


## Appointments

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `GET` | `/appointments` | index | List all appointments for current user |
| `POST` | `/appointments` | create | Book a new appointment (cancels any pending appointment) |
| `GET` | `/appointments/:id` | show | Show appointment details |
| `PUT` | `/appointments/:id` | update | Update appointment (reschedule or add notes) |
| `PATCH` | `/appointments/:id` | update | Partially update appointment |
| `DELETE` | `/appointments/:id` | destroy | Cancel appointment |
| `PUT` | `/appointments/:id/complete` | update | Mark appointment as completed |
| `GET` | `/appointments/current` | show | Get current active appointment |
| `GET` | `/appointments/history` | index | Get all completed appointments |

##  EHR (Electronic Health Records)

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `GET` | `/ehr` | index | Get all EHR records for current user |
| `POST` | `/ehr/notes` | create | Add a new note |
| `POST` | `/ehr/medications` | create | Add medication information |
| `GET` | `/ehr/:id` | show | Show specific EHR record |
| `PUT` | `/ehr/:id` | update | Update EHR record |
| `PATCH` | `/ehr/:id` | update | Partially update EHR record |
| `DELETE` | `/ehr/:id` | destroy | Delete EHR record |
| `GET` | `/ehr/notes` | index | Get all notes only |
| `GET` | `/ehr/medications` | index | Get all medications only |

## Reviews 

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `GET` | `/reviews` | index | Get all public reviews (displayed on website) |
| `POST` | `/reviews` | create | Add review (requires completed service) |
| `GET` | `/reviews/:id` | show | Show review details |
| `GET` | `/users/reviews` | index | Get all reviews by current user |
| `DELETE` | `/reviews/:id` | destroy | Delete own review |

</details>

### ERD Diagram w/ three models, User Model, & Relationships

- user model, appointmet mode (CRUD),Reviews (CRUD), Caregivers, Electronic Health Record(EHR)

<div align="center">
  <img src="https://raw.githubusercontent.com/RaghadAlbeladi1/GoldenCare-backend/main/for-readme/ERDraghad.png" width="900" alt="ERD Diagram" />
</div>

## User Stories

<details open>


| # | Role | Task |
|---|------|------|
| 1 | As a **user** | I want to **sign up** for an account |
| 2 | As a **user** | I want to **login** to my account |
| 3 | As a **user** | I want to **logout** from my account |
| 4 | As a **user** | I want to **view** my profile information |
| 5 | As a **user** | I want to **update** my profile information |
| 6 | As a **user** | I want to **delete** my account |
| 7 | As a **user** | I want to **view all** available services |
| 8 | As a **user** | I want to **view** service details |
| 9 | As a **user** | I want to **search** for services by name |
| 10 | As a **user** | I want to **view all** available caregivers |
| 11 | As a **user** | I want to **view** caregiver details |
| 12 | As a **user** | I want to **book** an appointment |
| 13 | As a **user** | I want to **choose duration** (day/month/3 months) when booking |
| 14 | As a **user** | I want to **select date and time** for my appointment |
| 15 | As a **user** | I want to **view all** my appointments |
| 16 | As a **user** | I want to **view** my current active appointment |
| 17 | As a **user** | I want to **view** my appointment history |
| 18 | As a **user** | I want to **update** my appointment details |
| 19 | As a **user** | I want to **add notes** to my appointment |
| 20 | As a **user** | I want to **cancel** my appointment |
| 21 | As a **user** | I want to **mark** my appointment as completed |
| 22 | As a **user** | I want to **add** a medical note |
| 23 | As a **user** | I want to **add** medication information |
| 24 | As a **user** | I want to **view all** my health records |
| 25 | As a **user** | I want to **view** only my notes |
| 26 | As a **user** | I want to **view** only my medications |
| 27 | As a **user** | I want to **update** my health records |
| 28 | As a **user** | I want to **delete** a health record |
| 29 | As a **user** | I want to **view all** public reviews |
| 30 | As a **user** | I want to **write** a review after completing service |
| 31 | As a **user** | I want to **rate** my experience (1-5 stars) |
| 32 | As a **user** | I want to **write comment** about my experience |
| 33 | As a **user** | I want to **view** my own reviews |
| 34 | As a **user** | I want to **delete** my reviews |

#### Review 
- User can write review **ONLY after completing service**
- Reviews will apear for all **visitors in public page**
- Rating with **1-5 stars** and write **comments and feedback**

</details>

## IceBox Features

Features planned for future implementation:

- Community Forum: Platform for families to connect, ask questions about best doctors, share experiences, and support each other
- Virtual Clinic: Virtual consultation sessions with healthcare professionals through the platform
- Advanced Medical Devices Section: Browse and request advanced medical devices, connected with contracted caregivers
- Emergency Response System: One-tap emergency button with instant caregiver and medical professional alert
- IoT Integration: Connect IoT devices for real-time health monitoring and automated alerts
- AI Health Agent: Intelligent AI assistant to answer health questions, provide recommendations, and guide users
- Comprehensive Dashboard: Real-time monitoring dashboard for families to track health metrics, appointments, and care status
- Smart Device Marketplace: Integration of cutting-edge technologies beneficial for elderly care
- Telemedicine Integration: Video consultations with doctors and specialists
- Medication Management: Smart medication reminders and tracking system
- Family Care Coordination: Dashboard for family members to coordinate care together
- Health Analytics: AI-powered insights into health trends and recommendations
- HL7 Integration: Health Level Seven (HL7) standard integration for seamless interoperability with hospitals, clinics, and other healthcare systems. HL7 enables standardized data exchange of patient records, lab results, prescriptions, and clinical documents, ensuring compatibility and secure communication between GoldenCare platform and external healthcare providers
- Comprehensive Patient Records: Progress notes, vitals tracking, and complete integrated patient information for holistic care management
- AI Medical Coder Agent: Intelligent AI agent for medical coding that accurately writes medical codes, calculates insurance claims, and ensures proper billing documentation
- Vitals Monitoring: Real-time tracking and recording of patient vital signs with historical data analysis
- Progress Notes System: Digital documentation of patient care progress, treatment updates, and medical observations

