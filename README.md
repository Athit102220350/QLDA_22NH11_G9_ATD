# English Learning Website

A comprehensive English learning platform with an AI-powered chatbot for grammar and vocabulary assistance, designed to help users improve their English language skills effectively.

## Features

- Homepage with information about the learning platform
- AI-powered chatbot for English grammar and vocabulary assistance
- Responsive design using Bootstrap 5
- User authentication and profile management
- Progress tracking for learners
- Interactive exercises and quizzes

## Setup and Installation

1. Clone the repository
   ```
   git clone https://github.com/Athit102220350/QLDA_22NH11_G9_ATD.git -b english-learning-website
   cd QLDA_22NH11_G9_ATD
   ```

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

5. Create a `.env` file in the root directory with the following variables:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

6. Run migrations:
   ```
   python manage.py migrate
   ```

7. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```
   python manage.py runserver
   ```

9. Access the website at http://127.0.0.1:8000/

## Technologies Used

- Django 5.0
- Python 3.11
- Bootstrap 5
- JavaScript/HTML/CSS
- SQLite (development) / PostgreSQL (production)
- Requests 2.31.0
- Gunicorn 21.2.0 (production server)



