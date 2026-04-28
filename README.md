# 📚 Library Management System

A full-stack Django web application for librarians to manage books, members, issuance, returns, and real-time analytics — deployed on Vercel with a Neon PostgreSQL backend.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-black?style=for-the-badge&logo=vercel)](https://librarymsystem.vercel.app/)
[![Django](https://img.shields.io/badge/Django-3.2-green.svg?logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg?logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-teal.svg?logo=postgresql)](https://neon.tech/)
[![UI](https://img.shields.io/badge/UI-Metronic%209%20Tailwind-blue.svg)](https://keenthemes.com/metronic)

## 🌐 Live Demo

**[View Live Application →](https://librarymsystem.vercel.app/)**

Deployed on Vercel with Neon PostgreSQL database and Google OAuth authentication.

---

## ✨ Features

### 📖 Book Management
- **CRUD Operations** — Add, update, delete books with inline bulk editing and bulk deletion
- **Advanced Search & Filter** — Search by title, filter by category (10+ options) and language (English / Urdu)
- **Smart Inventory** — Stock tracking with automatic low-stock alerts on the dashboard
- **Pagination** — All book lists paginated for performance

### 👥 Member Management
- **Student Registration** — Complete profiles with name, enrollment ID, phone, address, gender, and photo
- **Search & Filter** — Quick lookup by name or enrollment number, filter by gender
- **Bulk Operations** — Inline edit and bulk delete multiple members simultaneously

### ↩️ Issuance & Returns
- **Smart Issuance** — Select2 dropdowns for student and book selection with searchable UI
- **Flexible Return Dates** — Default 15-day return period, customisable per record
- **Auto Fine Calculation** — PKR 500 penalty auto-calculated for overdue books
- **Status Tracking** — Toggle between all issued books and overdue-only view
- **Inline Editing** — Edit issue/return dates directly in the table; confirm returns with modal

### 📊 Analytics Dashboard
- **Real-time Statistics** — Total books, issued count, overdue count, total members
- **Trend Charts** — 6-month line chart of issuance and return patterns (Chart.js)
- **Books Status** — Doughnut chart showing available vs issued vs overdue
- **Top Books** — Most frequently issued titles ranked by issue count
- **Activity Feed** — Latest 15 issuance events at a glance
- **Low Stock Alerts** — Books with quantity ≤ threshold flagged on dashboard

### 👤 Authentication & Profiles
- **Google OAuth** — One-click sign-in via django-allauth
- **Admin Signup / Login** — Standard username/password registration
- **User Profile** — View and edit name, email, phone, date of birth, address, and profile photo
- **Role-based Access** — All dashboard routes protected by `@login_required` + `@user_passes_test(is_admin)`

### 🎨 UI
- **Metronic 9 Tailwind** — Clean, minimal admin dashboard theme
- **Shared base template** — Single `base.html` with persistent sidebar and top header
- **Responsive sidebar** — Mobile toggle, active link highlighting
- **Consistent components** — Unified cards, tables, badges, buttons, and form styling throughout

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 3.2.25, Python 3.10 |
| Database (Dev) | SQLite |
| Database (Prod) | PostgreSQL via Neon (serverless) |
| Auth | django-allauth 0.54.0 + Google OAuth2 |
| Frontend | Django Templates, Metronic 9 Tailwind CSS, Chart.js, Bootstrap 5 (select pages) |
| Filtering | django-filter 23.5 |
| Static Files | WhiteNoise 6.11 |
| Deployment | Vercel (serverless) |
| WSGI Server | Gunicorn 21.2 |
| Image Processing | Pillow 12.1 |

---

## 🗂️ Project Structure

```
Library-Management-System-/
├── manage.py
├── requirements.txt
├── vercel.json                   ← Vercel deployment config
├── build_files.sh                ← migrate + collectstatic for Vercel build
├── Procfile                      ← Railway (legacy) start command
├── static/
│   ├── metronic/assets/          ← Metronic 9 compiled CSS, JS, favicon
│   │   ├── css/styles.css
│   │   ├── js/core.bundle.js
│   │   └── media/app/            ← favicon files only
│   ├── css/                      ← Legacy custom CSS (kept for reference)
│   ├── js/                       ← dashboard.js, userprofile.js
│   └── student/js/               ← viewbook.js, viewstudent.js, viewissuedbook.js
├── media/                        ← User-uploaded photos (dev only)
└── librarymanagement/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── library/
        ├── models.py             ← StudentExtra, Book, IssuedBook, AdminProfile
        ├── views.py              ← All business logic (FBVs)
        ├── urls.py               ← App URL patterns
        ├── forms.py              ← ModelForms and custom Forms
        ├── filters.py            ← BookFilter, StudentFilter (django-filter)
        ├── admin.py              ← Django admin registration
        ├── migrations/
        └── templates/
            ├── library/
            │   ├── base.html     ← Metronic sidebar + header shell
            │   ├── dashboard.html
            │   ├── viewbook.html
            │   ├── addbook.html
            │   ├── issuebook.html
            │   ├── viewissuedbook.html
            │   ├── userprofile.html
            │   ├── adminlogin.html
            │   ├── adminsignup.html
            │   ├── adminclick.html
            │   └── index.html
            └── student/
                ├── addstudent.html
                ├── viewstudent.html
                └── studentadded.html
```

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

# Set environment variables (optional — defaults to SQLite locally)
export DATABASE_URL=your_postgres_url
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
| `DATABASE_URL` | PostgreSQL connection string (falls back to SQLite if unset) |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret |
| `DEBUG` | `True` for dev, `False` for production |
| `EMAIL_HOST_USER` | Gmail address for system emails |
| `EMAIL_HOST_PASSWORD` | Gmail App Password  |

---

## 📖 Usage Guide

1. **Login** — via Google OAuth or admin credentials at `/adminclick`
2. **Add Books** — fill in title, author, quantity, category, language
3. **Register Students** — enter member info with enrollment ID
4. **Issue Books** — select student + book via searchable dropdowns, set return date
5. **Process Returns** — click Return on any issued record, confirm in modal
6. **Monitor** — dashboard shows trends, stock alerts, overdue items, and activity feed

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push and open a Pull Request

---

**Made with ❤️ by [Noor Butt](https://github.com/noorrbutt)**
