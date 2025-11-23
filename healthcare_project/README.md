# Healthcare Management System

A complete Django web application for healthcare management with role-based authentication.

## Features
- Email-based authentication
- Patient and Doctor portals
- Medical blog system
- Profile management
- Responsive Bootstrap UI

## Setup Instructions

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure MySQL database in settings.py

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Load blog categories:
```bash
python manage.py load_blog_categories
```

7. Run development server:
```bash
python manage.py runserver
```

## Default Login
Access admin panel at: http://127.0.0.1:8000/admin/
