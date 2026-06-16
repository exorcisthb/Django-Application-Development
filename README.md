# Django Application Development with SQL and Databases

This is a Django project for an online course platform with quiz functionality.

## Setup Instructions

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Django:
```bash
pip install django
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run server:
```bash
python manage.py runserver
```

## Project Structure

- `courses/` - Main Django app
  - `models.py` - Contains Course, Lesson, Question, Choice, Submission models
  - `admin.py` - Admin configuration
  - `views.py` - View functions
  - `urls.py` - URL patterns
  - `templates/` - HTML templates
