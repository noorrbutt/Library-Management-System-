from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from datetime import date
from . import forms, models
from librarymanagement.settings import EMAIL_HOST_USER



def home_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return render(request, 'library/index.html')


# for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return render(request, 'library/studentclick.html')


# for showing signup/login button for admin
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

            admin_group, created = Group.objects.get_or_create(name='ADMIN')
            admin_group.user_set.add(user)

            return redirect('adminlogin')
    return render(request, 'library/adminsignup.html', {'form': form})


def studentsignup_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    context = {'form1': form1, 'form2': form2}

    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            extra = form2.save(commit=False)
            extra.user = user
            extra.save()

            student_group, created = Group.objects.get_or_create(name='STUDENT')
            student_group.user_set.add(user)

            return redirect('studentlogin')

    return render(request, 'library/studentsignup.html', context=context)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return render(request, 'library/adminafterlogin.html')
    return render(request, 'library/studentafterlogin.html')


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
    books = models.Book.objects.all()
    return render(request, 'library/viewbook.html', {'books': books})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form = forms.IssuedBookForm()
    if request.method == 'POST':
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.enrollment = request.POST.get('enrollment2')
            obj.isbn = request.POST.get('isbn2')
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

        # Fine calculation
        days = (date.today() - ib.issuedate).days
        fine = max(0, (days - 15) * 10) if days > 15 else 0

        books = models.Book.objects.filter(isbn=ib.isbn)
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


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students = models.StudentExtra.objects.all()
    return render(request, 'library/viewstudent.html', {'students': students})


# -------------------- STUDENT VIEWS --------------------

@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student = models.StudentExtra.objects.get(user=request.user)
    issuedbooks = models.IssuedBook.objects.filter(enrollment=student.enrollment)

    book_info = []
    issue_info = []

    for ib in issuedbooks:
        books = models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            book_info.append((request.user, student.enrollment, student.branch, book.name, book.author))

        issdate = ib.issuedate.strftime('%d-%m-%Y')
        expdate = ib.expirydate.strftime('%d-%m-%Y')

        days = (date.today() - ib.issuedate).days
        fine = max(0, (days - 15) * 10) if days > 15 else 0

        issue_info.append((issdate, expdate, fine))

    return render(request, 'library/viewissuedbookbystudent.html', {'li1': book_info, 'li2': issue_info})


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
