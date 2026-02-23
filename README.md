# 📚 Library Management System

A comprehensive Django web application for librarians to efficiently manage library operations including books, members, issuance, returns, and real-time analytics.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Railway-blue?style=for-the-badge)](https://librarymanagementsystem.up.railway.app/)
[![Django](https://img.shields.io/badge/Django-3.2+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

## 🌐 Live Demo

**[View Live Application →](https://librarymanagementsystem.up.railway.app/)**

Deployed on Railway with PostgreSQL database.

---

## ✨ Features

### 📖 Book Management
- **CRUD Operations**: Add, update, delete books with bulk operations support
- **Advanced Search**: Filter by title, author, category (10+ categories), and language
- **Smart Inventory**: Inline editing, stock tracking with automatic low-stock alerts
- **Multi-language Support**: Manage books in English and Urdu
- **Categories**: Education, History, Novel, Fiction, Science, Technology, and more

### 👥 Member Management
- **Student Registration**: Complete profiles with name, enrollment ID, contact details, and photos
- **Search & Filter**: Quick lookup by name or enrollment number
- **Bulk Operations**: Efficient management of multiple members simultaneously
- **Profile Photos**: Upload and manage student profile pictures

### ↩️ Issuance & Returns
- **Smart Issuance**: Automatic availability checking before book issue
- **Flexible Return Dates**: Customizable return periods (default: 15 days)
- **Auto Fine Calculation**: PKR 500 penalty for overdue books
- **Status Tracking**: Monitor issued books, overdue items, and return history

### 📊 Analytics Dashboard
- **Real-time Statistics**: Total books, available inventory, issued books, active members, overdue count
- **Trend Analysis**: 6-month charts visualizing issuance and return patterns
- **Category Distribution**: Visual breakdown of library collection by genre
- **Top Books**: Track most frequently issued titles
- **Activity Feed**: Recent library activities at a glance
- **Alerts**: Low stock warnings and overdue notifications

### 👤 User Profile Management
- **Profile Updates**: Edit personal information and upload photos
- **Security**: Secure password management system
- **Account Settings**: Update email, phone, and address details

---

## 🛠️ Tech Stack

**Backend**
- Django 3.2+ - High-level Python web framework
- Python 3.8+ - Core programming language
- PostgreSQL - Production database (Railway deployment)
- SQLite - Local development database

**Frontend**
- Django Templates - Server-side rendering
- HTML5/CSS3 - Modern web standards
- JavaScript - Interactive features
- Chart.js - Data visualization for analytics

**Key Libraries**
- `django-filter` - Advanced filtering capabilities
- `django-widget-tweaks` - Form rendering customization
- `Pillow` - Image processing for profile photos
- `psycopg2` - PostgreSQL adapter

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### 💻 Local Installation

```bash
# Clone the repository
git clone https://github.com/noorrbutt/Library-Management-System-.git
cd Library-Management-System-

# Create and activate virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 🌐 Access the Application
Open your browser and navigate to: `http://127.0.0.1:8000/`

---

## 📖 Usage Guide

1. **Admin Registration**
   - Navigate to `/adminclick/`
   - Create admin account with signup form

2. **Login**
   - Use admin credentials to access dashboard
   - View real-time analytics and system overview

3. **Add Books**
   - Click "Add Book" from dashboard
   - Fill in book details (title, author, ISBN, category, language)
   - Submit to add to inventory

4. **Register Students**
   - Go to "Add Student" section
   - Enter member information and upload photo
   - Save to create student account

5. **Issue Books**
   - Select student from member list
   - Choose available book
   - Set return date and confirm issuance

6. **Manage Operations**
   - View all books, students, and issued books
   - Edit or delete records as needed
   - Process returns and calculate fines
   - Monitor analytics and trends

---

## 📁 Project Structure

```
Library-Management-System/
├── librarymanagement/           # Main Django project
│   ├── settings.py              # Project configuration
│   ├── urls.py                  # URL routing
│   └── library/                 # Core application
│       ├── models.py            # Database models (Book, Student, IssuedBook)
│       ├── views.py             # Business logic and controllers
│       ├── forms.py             # Django form definitions
│       ├── filters.py           # Search and filter logic
│       ├── admin.py             # Admin panel configuration
│       └── templates/           # HTML templates
│           ├── dashboard.html
│           ├── books/
│           ├── students/
│           └── issuance/
├── static/                      # Static assets
│   ├── css/                     # Stylesheets
│   ├── js/                      # JavaScript files
│   └── images/                  # Image assets
├── media/                       # User uploads (profile photos, etc.)
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── README.md                    # Documentation
```

---

## 🔧 Configuration

### Environment Variables (Production)
```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@host:port/dbname
ALLOWED_HOSTS=librarymanagementsystem.up.railway.app
```

### Database Setup
- **Development**: SQLite (no configuration needed)
- **Production**: PostgreSQL (configured via DATABASE_URL)

---

## 📸 Screenshots

- Dashboard with analytics
- Book management interface
- Student registration form
- Issuance tracking page

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch 
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📝 License

This project is open source and available for educational purposes.

---

**Made with ❤️ by Noor Butt**
