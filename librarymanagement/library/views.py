from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from datetime import date
from . import forms, models
from librarymanagement.settings import EMAIL_HOST_USER
from .models import Book
from .filters import BookFilter
import json

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
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_books_view(request):
    if request.method == "POST":
        selected_books = request.POST.getlist("selected_books")
        if selected_books:
            models.Book.objects.filter(id__in=selected_books).delete()
    return redirect("viewbook")

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_books_view(request):
    if request.method == "POST":
        books_data = json.loads(request.POST.get("books_data", "[]"))
        for book_data in books_data:
            book = models.Book.objects.get(id=book_data["id"])
            book.name = book_data["name"]
            book.quantity = book_data["quantity"]
            book.author = book_data["author"]
            book.category = book_data["category"]
            book.language = book_data["language"]
            book.save()
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
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            user.set_password(user.password)
            user.save()
            extra = form2.save(commit=False)
            extra.user = user
            extra.save()
            student_group, _ = Group.objects.get_or_create(name='STUDENT')
            student_group.user_set.add(user)
            return redirect('studentadded')
    return render(request, 'student/addstudent.html', {'form1': form1, 'form2': form2})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students = models.StudentExtra.objects.all()
    return render(request, 'student/viewstudent.html', {'students': students})

# -------------------- INFO PAGES --------------------

def aboutus_view(request):
    return render(request, 'library/aboutus.html')

def contactus_view(request):
    form = forms.ContactusForm()
    if request.method == 'POST':
        form = forms.ContactusForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            name = form.cleaned_data['Name']
            message = form.cleaned_data['Message']
            send_mail(
                f"{name} || {email}",
                message,
                EMAIL_HOST_USER,
                ['wapka1503@gmail.com'],
                fail_silently=False
            )
            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactus.html', {'form': form})

def studentadded_view(request):
    return render(request, 'student/studentadded.html')
