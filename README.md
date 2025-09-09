Ecommerce Django Project with AI
Project Overview

A full-featured Ecommerce web application built with Django and Python, featuring AI-based recommendations. Users can browse products, manage shopping carts, and place orders, while AI enhances personalized suggestions and search functionality.

---

Features

User Authentication: Secure login, signup, and profile management.

Product Management: Add, update, delete, and view products with images.

Shopping Cart & Orders: Manage cart, checkout, and order tracking.

AI Recommendations: Personalized product suggestions using AI.

Search Functionality: Enhanced product search with AI/NLP.

Admin Dashboard: Manage products, categories, users, and orders.

Responsive Design: Optimized for desktop, tablet, and mobile devices.

---

Technologies Used

Backend: Django, Python

Frontend: HTML5, CSS3, Bootstrap

Database: SQLite (upgradeable to PostgreSQL/MySQL)

AI/ML: Python-based recommendation engine

Tools: Git, GitHub

---

Installation

Clone the repository:

git clone https://github.com/seenivasan-offl/Ecommerce-django-using-AI.git


Navigate to the project directory:

cd Ecommerce-django-using-AI

---

Create a virtual environment:

python -m venv env
# Linux/Mac
source env/bin/activate
# Windows
env\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Run the development server:

python manage.py runserver

---

Open your browser at http://127.0.0.1:8000/

---

Project Structure

ecom_project/ – Main Django project

ecom_app/ – Application with models, views, templates

media/product_images/ – Uploaded product images

static/ – CSS, JS, and frontend assets

requirements.txt – Project dependencies

db.sqlite3 – Database file

---

Future Enhancements

Integrate a payment gateway (Razorpay/Stripe).

Upgrade AI recommendations using deep learning models.

Add user reviews and ratings.

Implement real-time notifications for orders and promotions.

---

Author

Seenivasan H

GitHub: seenivasan-offl

LinkedIn: https://www.linkedin.com/in/seeni-vasan-h
