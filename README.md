# Django Healthcare Management System

A complete, production-ready healthcare web application built with Django 4.2.7 and MySQL. Features role-based authentication for Patients and Doctors with distinct dashboards, profile management, and an integrated medical blog system.

---

## 🏥 Features

### Authentication System
- **Email-Based Login**: Secure authentication using email and password (no username required)
- **Custom User Model**: Extended Django AbstractUser with role-based access
- **Two User Roles**: Patient and Doctor with distinct capabilities
- **Profile Management**: Image uploads, address information, and role-specific details

### Patient Portal
- **Personal Dashboard**: View medical information and profile details
- **Medical Records**: Track medical history, allergies, blood group, emergency contacts
- **Health Blog Access**: Browse and read published health articles across 4 categories
- **Category Filtering**: Easy navigation through Medical topics

### Doctor Portal
- **Professional Dashboard**: Display specialization, license, experience, and consultation fees
- **Blog Management**: Full CRUD operations for medical blog posts
- **Draft System**: Save drafts before publishing
- **Analytics**: View total and published post counts

### Blog System
- **4 Medical Categories**: Mental Health, Heart Disease, COVID-19, Immunization
- **Rich Content**: Title, featured image, summary (max 500 chars), full content
- **Status Control**: Draft or Published states
- **Author Attribution**: Automatic doctor profile linking
- **Summary Preview**: First 15 words displayed in card views

---

## 📁 Project Structure

```
healthcare_project/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── healthcare_project/          # Main project settings
│   ├── __init__.py
│   ├── settings.py              # MySQL config, installed apps
│   ├── urls.py                  # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                    # User authentication & profiles
│   ├── migrations/
│   ├── templates/accounts/
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── patient_dashboard.html
│   │   ├── doctor_dashboard.html
│   │   ├── patient_profile_update.html
│   │   └── doctor_profile_update.html
│   ├── management/commands/     # Custom management commands
│   ├── models.py                # CustomUser, PatientProfile, DoctorProfile
│   ├── views.py                 # Auth views, dashboards, profile updates
│   ├── forms.py                 # SignUp, Login, Profile forms
│   ├── managers.py              # CustomUserManager for email auth
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
│
├── blog/                        # Medical blog system
│   ├── migrations/
│   ├── templates/blog/
│   │   ├── blog_list.html
│   │   ├── blog_detail.html
│   │   ├── blog_form.html
│   │   ├── my_posts.html
│   │   └── blog_confirm_delete.html
│   ├── management/commands/
│   │   └── load_blog_categories.py
│   ├── models.py                # BlogCategory, BlogPost
│   ├── views.py                 # CRUD operations for blogs
│   ├── forms.py                 # BlogPostForm
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
│
├── templates/                   # Base templates
│   └── base.html                # Bootstrap 5 navigation
│
├── static/                      # CSS, JavaScript
│   ├── css/
│   └── js/
│
└── media/                       # User uploads
    ├── profiles/                # Profile images
    └── blog_images/             # Blog featured images
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+ or MariaDB
- pip (Python package manager)

### Step 1: Extract Project
```bash
unzip healthcare_management_system.zip
cd healthcare_project
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies:**
- Django==4.2.7
- mysqlclient==2.2.0
- Pillow==10.1.0

### Step 4: Configure MySQL Database

Create a MySQL database:
```sql
CREATE DATABASE healthcare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'healthcare_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON healthcare_db.* TO 'healthcare_user'@'localhost';
FLUSH PRIVILEGES;
```

Update `healthcare_project/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'healthcare_db',
        'USER': 'healthcare_user',
        'PASSWORD': 'your_password',  # Change this
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Load Blog Categories
```bash
python manage.py load_blog_categories
```

This creates the 4 predefined medical categories:
- Mental Health
- Heart Disease
- COVID-19
- Immunization

### Step 7: Create Superuser
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Access the application at: `http://127.0.0.1:8000`

---

## 🔑 Usage Guide

### User Registration
1. Navigate to `http://127.0.0.1:8000/accounts/signup/`
2. Fill in email, name, user type (Patient/Doctor), and password
3. Submit to create account and auto-login

### Patient Workflow
1. **Login** → Redirected to Patient Dashboard
2. **View Profile** → See medical information card
3. **Update Profile** → Add medical history, allergies, blood group, etc.
4. **Browse Blogs** → Access all published health articles
5. **Filter by Category** → Click category buttons to filter content

### Doctor Workflow
1. **Login** → Redirected to Doctor Dashboard
2. **View Profile** → See professional information and blog stats
3. **Update Profile** → Add specialization, license, fees, bio
4. **Create Blog Post** → Click "Create New Post"
   - Add title, category, featured image
   - Write summary (max 500 characters)
   - Compose full content
   - Choose Draft or Published status
5. **Manage Posts** → View "My Posts" to edit or delete
6. **Preview Published** → Click "View" to see public version

### Admin Panel
Access at `http://127.0.0.1:8000/admin/`
- Manage all users, profiles, blogs, and categories
- Approve doctor registrations
- Moderate blog content

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 4.2.7 |
| **Database** | MySQL 5.7+ |
| **Frontend** | Bootstrap 5, HTML5, CSS3 |
| **Authentication** | Django Custom User Model |
| **Image Processing** | Pillow |
| **Server** | Django Development Server / Gunicorn (production) |

---

## 📊 Database Models

### CustomUser
- Email-based authentication (no username)
- User type: Patient or Doctor
- Profile image, phone, address fields
- Links to PatientProfile or DoctorProfile

### PatientProfile
- Medical history (text)
- Allergies
- Blood group (dropdown)
- Date of birth
- Emergency contact

### DoctorProfile
- Specialization (6 options)
- Medical license number (unique)
- Years of experience
- Consultation fee
- Professional bio
- Qualification

### BlogCategory
- Name (unique)
- Auto-generated slug
- Description
- 4 predefined categories

### BlogPost
- Title (unique) with auto-slug
- Author (ForeignKey to Doctor)
- Category (ForeignKey to BlogCategory)
- Featured image
- Summary (max 500 chars)
- Full content
- Status: Draft or Published
- Timestamps

---

## 🔒 Security Features

- CSRF protection on all forms
- Password validation (Django validators)
- SQL injection protection (Django ORM)
- XSS protection (template auto-escaping)
- Secure file uploads (Pillow validation)
- Login required decorators
- Permission checks (doctors only for blog management)

---

## 🎨 UI/UX Features

- **Responsive Design**: Mobile-friendly Bootstrap 5 layout
- **Color Scheme**: Healthcare-themed teal primary color
- **Navigation**: Context-aware navbar (changes based on auth status)
- **Messages**: Flash messages for user feedback
- **Cards**: Clean card-based layouts for content display
- **Forms**: Styled Bootstrap form controls with validation

---

## 📝 Management Commands

### Load Blog Categories
```bash
python manage.py load_blog_categories
```
Creates the 4 predefined medical blog categories.

### Create Superuser
```bash
python manage.py createsuperuser
```
Creates an admin account for the Django admin panel.

---

## 🚢 Production Deployment

### Environment Variables
Set these in production:
- `SECRET_KEY`: Generate a new secure key
- `DEBUG`: Set to `False`
- `ALLOWED_HOSTS`: Add your domain
- `DATABASE_URL`: Production database credentials

### Static Files
```bash
python manage.py collectstatic
```

### WSGI Server
Use Gunicorn or uWSGI:
```bash
gunicorn healthcare_project.wsgi:application
```

### Nginx Configuration
Configure Nginx as reverse proxy for static/media files.

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 📞 Support

For issues or questions about setup, refer to the Django documentation or MySQL guides.

---

**Built with ❤️ using Django Framework**
