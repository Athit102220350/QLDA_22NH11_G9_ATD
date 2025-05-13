# English Learning Website

A basic English learning website with an AI chatbot for grammar and vocabulary assistance.

## Features

- Homepage with information about the learning platform
- AI-powered chatbot for English grammar and vocabulary assistance
- Responsive design using Bootstrap 5

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```
   python manage.py migrate
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```
7. Access the website at http://127.0.0.1:8000/

## Technologies Used

- Django 5.0
- Python 3.11
- Bootstrap 5
- JavaScript/HTML/CSS

## Project Structure

```
english_learning_website/
├── core/                      # Main app
│   ├── static/                # Static files
│   │   ├── css/               # CSS files
│   │   └── js/                # JavaScript files
│   ├── templates/             # HTML templates
│   │   ├── base.html          # Base template with common elements
│   │   ├── index.html         # Homepage
│   │   └── chatbot.html       # Chatbot interface
│   ├── admin.py               # Admin settings
│   ├── apps.py                # App configuration
│   ├── models.py              # Database models
│   ├── tests.py               # Tests
│   ├── urls.py                # URL routing for core app
│   └── views.py               # View functions
├── english_learning_website/  # Project settings
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
└── manage.py                  # Django management script
```
