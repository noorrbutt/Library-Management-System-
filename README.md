# 📚 Library Management System

A comprehensive Django web application for librarians to manage library operations including books, members, issuance, returns, and analytics.

![Django](https://img.shields.io/badge/Django-3.2+-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

## ✨ Features

### Book Management
- Add, update, delete books with bulk operations
- Advanced search by title, author, category (10+ categories), and language
- Inline editing and stock tracking with low-stock alerts
- Filter by category (Education, History, Novel, Fiction, etc.) and language (English/Urdu)

### Member Management
- Register students with complete profiles (name, enrollment, address, phone, gender, photo)
- Search by name or enrollment number
- Bulk operations and inline editing

### Issuance & Returns
- Smart book issuance with availability checking
- Custom return dates (default: 15 days)
- Automatic fine calculation (PKR 500 for overdue books)
- Track issued and overdue books

### Analytics Dashboard
- Real-time statistics (total books, available, issued, members, overdue)
- 6-month trend charts for issued and returned books
- Category distribution and top 5 most issued books
- Recent activities feed and low stock alerts

### User Profile
- Update personal information and profile photo
- Secure password management
- Account settings (email, phone, address)

## 🛠️ Tech Stack

- **Backend**: Django 3.2+, Python 3.8+
- **Database**: SQLite (default), PostgreSQL-ready
- **Frontend**: Django Templates, HTML5, CSS3, JavaScript, Chart.js
- **Key Libraries**: django-filter, django-widget-tweaks, Pillow

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/noorrbutt/Library-Management-System-.git
cd Library-Management-System-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Access
- Main App: http://127.0.0.1:8000/
- Dashboard: http://127.0.0.1:8000/dashboard/
- Admin Panel: http://127.0.0.1:8000/admin/

## 📖 Usage

1. **Register** - Go to /adminclick/ and signup as admin
2. **Login** - Use admin credentials to access dashboard
3. **Add Books** - Navigate to Add Book, fill details, and submit
4. **Add Students** - Go to Add Student and register members
5. **Issue Books** - Select student and book, set return date
6. **Manage** - View, edit, delete, or return books from respective pages

## 📁 Project Structure

```
Library-Management-System/
├── librarymanagement/
│   ├── settings.py
│   ├── urls.py
│   └── library/
│       ├── models.py       # Book, Student, IssuedBook
│       ├── views.py        # Business logic
│       ├── forms.py        # Form definitions
│       ├── filters.py      # Filtering logic
│       └── templates/      # HTML templates
├── static/                 # CSS, JS, images
├── media/                  # User uploads
├── manage.py
└── requirements.txt
```


## 🤝 Contributing

Contributions are welcome! Fork the repo, create a feature branch, and submit a PR.

---

Made with ❤️
