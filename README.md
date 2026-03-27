# 📚 Library Management System

A full-stack Django web application for librarians to manage books, members, issuance, returns, and real-time analytics — deployed on Vercel with a Neon PostgreSQL backend.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-black?style=for-the-badge&logo=vercel)](https://librarymsystem.vercel.app/)
[![Django](https://img.shields.io/badge/Django-3.2-green.svg?logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg?logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-teal.svg?logo=postgresql)](https://neon.tech/)

## 🌐 Live Demo

**[View Live Application →](https://librarymsystem.vercel.app/)**

Deployed on Vercel with Neon PostgreSQL database and Google OAuth authentication.

---

## ✨ Features

### 📖 Book Management
- **CRUD Operations**: Add, update, delete books with bulk operations support
- **Advanced Search**: Filter by title, author, category (10+ categories), and language
- **Smart Inventory**: Stock tracking with automatic low-stock alerts
- **Multi-language Support**: English and Urdu books
- **Categories**: Education, History, Novel, Fiction, Science, Technology, and more

### 👥 Member Management
- **Student Registration**: Complete profiles with name, enrollment ID, contact details, and address
- **Search & Filter**: Quick lookup by name or enrollment number
- **Bulk Operations**: Efficient management of multiple members simultaneously

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

### 👤 Authentication
- **Google OAuth**: One-click sign-in via django-allauth
- **Role-based Access**: Admin and librarian access levels
- **Secure Sessions**: HTTPS enforced on production

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 3.2, Python 3.10 |
| Database | PostgreSQL (Neon) |
| Auth | django-allauth + Google OAuth |
| Frontend | Django Templates, HTML5/CSS3, JavaScript, Chart.js |
| Deployment | Vercel |
| Static Files | WhiteNoise |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip
- Git

### 💻 Local Installation

```bash
# Clone the repository
git clone https://github.com/noorrbutt/Library-Management-System-.git
cd Library-Management-System-

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=your_postgres_url   # or use SQLite by default
export GOOGLE_CLIENT_ID=your_client_id
export GOOGLE_CLIENT_SECRET=your_client_secret

# Setup database
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/`

---

## ⚙️ Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | PostgreSQL connection string |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret |
| `DEBUG` | `True` for dev, `False` for production |

---

## 🗂️ Project Structure

```
Library-Management-System/
├── librarymanagement/
│   ├── settings.py
│   ├── urls.py
│   └── library/
│       ├── models.py        # Book, Student, IssuedBook
│       ├── views.py
│       ├── forms.py
│       ├── filters.py
│       ├── admin.py
│       └── templates/
├── static/
├── media/
├── requirements.txt
└── manage.py
```

---

## 📖 Usage Guide

1. **Login** via Google OAuth or admin credentials
2. **Add Books** — fill in title, author, quantity, category, language
3. **Register Students** — enter member info and upload photo
4. **Issue Books** — select student + book, set return date
5. **Process Returns** — mark returned, fines auto-calculated
6. **Monitor Analytics** — dashboard shows trends, stock alerts, overdue items

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and open a Pull Request

---

**Made with ❤️ by [Noor Butt](https://github.com/noorrbutt)**
