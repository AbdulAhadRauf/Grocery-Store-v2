# Grocery-Store-V2

## Introduction
  Grocery-Store-V2 is a versatile Grocery Store Application developed with Flask and Vue. This application implements Role-Based Access Control (RBAC) for users, store managers, and administrators, allowing permission-based requests for CRUD operations on categories and products.

## Features

**User Management**
User Authentication: Token-based authentication for secure signup and login.

Account Management: Create, view, edit, and delete user accounts.

**Category and Product Management**
Category Management: Create, view, edit, and delete product categories.

Product Management: Create, view, edit, and delete products.

**Request Handling**
Request Management: Create, view, and delete user requests.
**API Functionality**
RESTful API: Well-defined API for posts, users, comments, and follows.
**Asynchronous Jobs**
User-Triggered Async Jobs: Download user posts as a CSV file.

Daily Reminder Jobs: Receive daily reminders for posting.

Scheduled Jobs: Monthly engagement report delivered as an email or PDF.

**Performance and Caching**
Strategic caching and cache expiry for enhanced API performance.



## Technologies Used
## Backend
Flask: Lightweight and flexible Python web framework.

Jinja2 Templates: Used for rendering HTML templates and sending emails.

SQLite and SQLAlchemy: Storage and ORM tool for data management.

Flask-Restful: Development of the RESTful API.

Flask-SQLAlchemy: Database access and modification.

Flask-Celery: Management of asynchronous background jobs.

Flask-Caching: Performance optimization through API output caching.

Redis: In-memory database for API cache and message broker for Celery.

## Frontend
VueJS: JavaScript framework for building the frontend UI.

Bootstrap: Styling and UI components for an attractive and responsive interface.

## Setup Instructions
Ensure Redis and MailHog are installed and running:

redis-server
mailhog


Execute the following commands:


python main.py
## Workers:
celery -A main.celery worker -l info

##  Beats:
celery -A main.celery beat --max-interval 1 -l info

##  Getting Started
Follow these steps to set up and run the Grocery-Store-V2 application on your local environment.

## Contributing
If you'd like to contribute to the project, please follow the guidelines in CONTRIBUTING.md.

## License
This project is licensed under the MIT License.