Ecommerce Django Project with AI
Project Overview

This is a full-featured Ecommerce web application built using Django as the backend framework and Python for AI-based features. The platform allows users to browse products, manage shopping carts, and make purchases while leveraging AI for personalized recommendations and product search enhancements.

Features

User Authentication: Secure login, signup, and user management using Django's authentication system.

Product Management: CRUD operations for products including images and details.

Shopping Cart & Orders: Add products to cart, manage quantities, and place orders.

AI-based Recommendations: Personalized product suggestions based on user behavior and preferences.

Search Functionality: Enhanced search using AI/NLP techniques.

Admin Dashboard: Manage products, categories, users, and orders easily.

Responsive Design: Works seamlessly across desktop, tablet, and mobile devices.

Technologies Used

Backend: Django, Python

Frontend: HTML5, CSS3, Bootstrap

Database: SQLite (can be upgraded to PostgreSQL/MySQL)

AI/ML: Python-based recommendation engine for products

Tools: Git, GitHub

Installation

Clone the repository:

git clone https://github.com/seenivasan-offl/Ecommerce-django-using-AI.git


Navigate to the project directory:

cd Ecommerce-django-using-AI


Create a virtual environment:

python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Run the development server:

python manage.py runserver


Open your browser at http://127.0.0.1:8000/

Project Structure

ecom_project/ – Main Django project folder

ecom_app/ – Main application with models, views, and templates

media/product_images/ – Stores uploaded product images

static/ – Contains CSS, JS, and frontend assets

requirements.txt – List of dependencies

db.sqlite3 – SQLite database file

Future Enhancements

Integrate payment gateway (Razorpay/Stripe).

Upgrade AI recommendations using deep learning models.

Implement user review and rating system.

Add real-time notifications for orders and promotions.

Author

Seenivasan H

GitHub: seenivasan-offl

LinkedIn: https://www.linkedin.com/in/seeni-vasan-h
