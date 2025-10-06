# Library System

A simple Django-based library system with **users, librarians, and admin** roles, supporting book lending and notifications.

---
## Technology Stack

- Python 3.12+  
- Django 5.x
- Django REST Framework  
- SQLite  
---

## Features

### User Roles
- **SuperAdmin (Django superuser)**: Full system access.  
- **Librarian**: Create, manage books, and view/update lendings.  
- **User**: View books.  

### Book Lending
- Users can borrow books.  
- **Payments are simulated**: automatically marked as completed after 10 seconds via a Celery task.  

### Email Notifications
- Notify librarian/admin when a book is purchased.  
- Notify user when the book return date is due.  

### API Endpoints
- User registration, login, and token refresh.  
- Book CRUD operations (for librarians/admin).  
- Lending CRUD operations


## 🚀 Getting Started

Follow the steps below to set up and run the library System on your local machine.

---

### 1. Clone the Repository

Start by cloning the project from GitHub:

```bash
git clone https://github.com/Ananthu303/library-system.git
cd library_system
```

### 2. Create and Activate a Virtual Environment

It is recommended to use a virtual environment to manage dependencies for this project. Here’s how to create and activate it:

For **Windows**:
```bash
python -m venv venv

venv\Scripts\activate
```

For **macOS/Linux**:
```bash
python3 -m venv venv

source venv/bin/activate
```

Once activated, your terminal should show something like `(venv)` indicating that the virtual environment is active.

### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

Apply the database migrations to set up the necessary database schema:

```bash
python manage.py migrate
```

### 5. Create Superuser (Super Admin)

You need to create a superuser.
Run the following command to create the superuser:

```bash
python manage.py createsuperuser
```

You will be prompted to enter the following information:

- Username
- Email
- Password

This superuser is the SUPERADMIN having full control over the system

### 6. Run the Development Server

Once everything is set up, run the Django development server:

```bash
python manage.py runserver
```

Now, you can access the API's at `http://127.0.0.1:8000/`.

---

### 7. Celery Setup (Background Tasks & Notifications)


## 1. Start Redis Server

Celery requires **Redis** as a message broker. Make sure Redis is running:

```bash
redis-server
```

## 2. Start Celery Worker

Open a new terminal and run:

```bash
celery -A library_system worker -l info
```
add --pool=solo is required on Windows.

## 3. Start Celery Beat (Scheduler)

Open another terminal and run:

```bash
celery -A library_system beat -l info
```
Beat schedules periodic tasks such as daily due-date notifications to users.
In the admin panel, you can configure tasks and schedules using django-celery-beat.

## 4 Due-Date Notifications

- The system automatically notifies users when their book return date arrives.
- This is handled by a Celery periodic task running once per day.
- Ensure the task is enabled in Celery Beat and the schedule is correctly set in the admin panel to run once per day.

## Notes
- Payments are simulated and marked as completed automatically via Celery after 10 seconds.
- Keep the worker and beat terminals running for background tasks and scheduled notifications.
- Email notifications use SMTP and require a valid email configured in .env. check .env_sample
