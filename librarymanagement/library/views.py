from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from datetime import date
from . import forms, models
from librarymanagement.settings import EMAIL_HOST_USER
from .models import Book
from .filters import BookFilter, StudentFilter
from django.contrib import messages
import json
from django.http import HttpResponse


# -------------------- BASIC VIEWS --------------------

def home_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return render(request, 'library/index.html')


def adminclick_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return render(request, 'library/adminclick.html')


def adminsignup_view(request):
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            admin_group, _ = Group.objects.get_or_create(name='ADMIN')
            admin_group.user_set.add(user)
            return redirect('adminlogin')
    return render(request, 'library/adminsignup.html', {'form': form})


# -------------------- ROLE CHECK --------------------

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


# -------------------- AFTER LOGIN --------------------

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request, 'library/adminafterlogin.html')
    return redirect('adminlogin')


# -------------------- ADMIN VIEWS --------------------

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    form = forms.BookForm()
    if request.method == 'POST':
        form = forms.BookForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'library/bookadded.html')
    return render(request, 'library/addbook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books = Book.objects.all()

    # Search query
    query = request.GET.get('q', '')
    if query:
        books = books.filter(name__icontains=query)

    # Apply filters using BookFilter
    book_filter = BookFilter(request.GET, queryset=books)
    books = book_filter.qs

    # Prepare choices for template (using display labels from model choices)
    category_choices = Book.catchoice
    language_choices = Book.langchoice

    return render(request, 'library/viewbook.html', {
        'books': books,
        'filter': book_filter,
        'query': query,
        'category_choices': category_choices,
        'language_choices': language_choices,
    })


from django.contrib import messages

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_books_view(request):
    if request.method == "POST":
        selected_books = request.POST.getlist("selected_books")  # get list of selected book IDs
        if selected_books:
            models.Book.objects.filter(id__in=selected_books).delete()
            messages.success(request, f"{len(selected_books)} book(s) deleted successfully!")
        else:
            messages.warning(request, "No books selected for deletion.")
        return redirect("viewbook")
    return redirect("viewbook")


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_books_view(request):
    if request.method == "POST":
        import json
        books_data = json.loads(request.POST.get("books_data", "[]"))

        for book_data in books_data:
            book = models.Book.objects.get(id=book_data["id"])
            book.name = book_data["name"]
            book.quantity = book_data["quantity"]
            book.author = book_data["author"]
            book.category = book_data["category"]
            book.language = book_data["language"]
            book.save()

        messages.success(request, "Books updated successfully!")
        return redirect("viewbook")
    return redirect("viewbook")


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form = forms.IssuedBookForm()
    if request.method == 'POST':
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.enrollment = request.POST.get('enrollment2')
            obj.quantity = request.POST.get('quantity2')
            obj.save()
            return render(request, 'library/bookissued.html')
    return render(request, 'library/issuebook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks = models.IssuedBook.objects.all()
    data = []
    for ib in issuedbooks:
        issdate = ib.issuedate.strftime('%d-%m-%Y')
        expdate = ib.expirydate.strftime('%d-%m-%Y')
        days = (date.today() - ib.issuedate).days
        fine = max(0, (days - 15) * 10) if days > 15 else 0
        books = models.Book.objects.filter(quantity=ib.quantity)
        students = models.StudentExtra.objects.filter(enrollment=ib.enrollment)
        for student, book in zip(students, books):
            data.append((
                student.get_name,
                student.enrollment,
                book.name,
                book.author,
                issdate,
                expdate,
                fine
            ))
    return render(request, 'library/viewissuedbook.html', {'li': data})


# -------------------- STUDENT VIEWS --------------------

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addstudent_view(request):
    form = forms.StudentExtraForm()
    if request.method == 'POST':
        form = forms.StudentExtraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studentadded')
    return render(request, 'student/addstudent.html', {'form': form})

def studentadded_view(request):
    return render(request, 'student/studentadded.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students = models.StudentExtra.objects.all()
    
    # Initialize filter - use StudentFilter directly
    student_filter = StudentFilter(request.GET, queryset=students)
    students = student_filter.qs
    
    # Search functionality (additional to filter)
    query = request.GET.get('q', '').strip()
    if query and query != 'None':  # Handle the "None" string case
        students = students.filter(name__icontains=query)
    
    return render(request, 'student/viewstudent.html', {
        'students': students,
        'filter': student_filter,
        'query': query if query != 'None' else '',  # Convert "None" to empty string
        'gender_choices': models.StudentExtra.genchoice
    })

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_students_view(request):
    if request.method == "POST":
        selected_students = request.POST.getlist("selected_students")
        if selected_students:
            models.StudentExtra.objects.filter(id__in=selected_students).delete()
            messages.success(request, f"{len(selected_students)} Student(s) deleted successfully!")
        else:
            messages.warning(request, "No student selected for deletion.")
        return redirect("viewstudent")
    return redirect("viewstudent")


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_students_view(request):
    if request.method == "POST":
        students_data = json.loads(request.POST.get("students_data", "[]"))
        for student_data in students_data:
            student = models.StudentExtra.objects.get(id=student_data["id"])
            student.name = student_data["name"]
            student.enrollment = student_data["enrollment"]
            student.address = student_data["address"]
            student.phone = student_data["phone"]
            student.gender = student_data["gender"]
            student.save()
            
        messages.success(request, "Student(s) updated successfully!")
        return redirect("viewstudent")
    return redirect("viewstudent")