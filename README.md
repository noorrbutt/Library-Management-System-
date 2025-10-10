# Library Management System

A web application for librarians to create, track, and manage library data (books, members, borrowing, etc.).

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Installation & Setup](#installation--setup)  
- [Usage](#usage)  
- [Database](#database)  

## Features

- Add, update, delete books  
- Add, update, delete library members  
- Issue and return books  
- Track book availability  
- Search books by title, author, quantity  
- Simple user interface for librarians  
- Static assets (images, CSS, etc.)  
- Template-driven pages  

## Tech Stack

- **Backend / Framework**: Django (Python)  
- **Frontend / Templating**: Django templates, HTML, CSS  
- **Database**: SQLite (default)  
- **Static files / Images**  
- **Python packages** listed in `requirements.txt`  

## Installation & Setup

Follow these steps to run the project locally:

1. **Clone the repository**  
   ```bash
   git clone https://github.com/noorrbutt/Library-Management-System-.git
   cd Library-Management-System-
   ```

2. **Set up a virtual environment** (recommended)  
   ```bash
   python3 -m venv venv
   source venv/bin/activate     # on Unix / macOS  
   venv\Scripts\activate        # on Windows  
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Database migrations**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server**  
   ```bash
   python manage.py runserver
   ```

6. **Access in browser**  
   Go to `http://127.0.0.1:8000/` (or whichever port Django says)  

## Usage

- Use the web interface to add books, members.  
- Issue books to members; mark returns.  
- Search for books.  
- Manage data from the admin interface (if enabled).  

You may want to create a **superuser** to access Django’s admin:

```bash
python manage.py createsuperuser
```

## Database

- The project uses **SQLite** out of the box (`db.sqlite3`).  
- You can change to another database (e.g. PostgreSQL, MySQL) by adjusting `settings.py`.  
- Make sure to update `DATABASES` config and install relevant DB drivers.  
