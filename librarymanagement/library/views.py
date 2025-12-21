from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from datetime import date, datetime, timedelta
from . import forms, models
from librarymanagement.settings import EMAIL_HOST_USER
from .models import Book, StudentExtra, IssuedBook
from .filters import BookFilter, StudentFilter
from django.contrib import messages
import json
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count


# -------------------- ROLE CHECK --------------------

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


# -------------------- BASIC VIEWS --------------------

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'library/index.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def dashboard_view(request):
    """
    Comprehensive dashboard displaying library statistics and metrics.
    """
    today = date.today()
    month_start = today.replace(day=1)
    
    # ========== BASIC STATISTICS ==========
    total_books = Book.objects.count()
    total_members = StudentExtra.objects.count()
    
    # Issued books (currently not returned)
    issued_books_count = IssuedBook.objects.filter(returned=False).count()
    
    # Available books
    available_books_count = Book.objects.filter(quantity__gt=0).count()
    
    # Overdue books (past return date and not returned)
    overdue_books_count = IssuedBook.objects.filter(
        return_date__lt=today,
        returned=False
    ).count()
    
    # Books added this month (new books created this month)
    books_this_month = Book.objects.filter(
        id__gte=Book.objects.filter(
            id__in=IssuedBook.objects.filter(
                issuedate__gte=month_start
            ).values_list('book_id', flat=True)
        ).count()
    ).count()
    
    # If the above logic is wrong, use this simpler version:
    # books_this_month = Book.objects.filter(
    #     created_at__gte=month_start  # Assuming you have a created_at field
    # ).count()
    
    # ========== RECENT ACTIVITIES ==========
    recent_activities = IssuedBook.objects.select_related(
        'student', 'book'
    ).order_by('-issuedate')[:15]
    
    # ========== TOP 5 MOST ISSUED BOOKS ==========
    top_books = Book.objects.annotate(
        issue_count=Count('issuedbook')
    ).filter(
        issue_count__gt=0  # Only books that have been issued
    ).order_by('-issue_count')[:5]
    
    # ========== MONTHLY TRENDS (Last 6 Months) ==========
    months_data = []
    issued_trend = []
    returned_trend = []
    
    for i in range(5, -1, -1):  # Last 6 months
        month_date = today - timedelta(days=30 * i)
        month_start_calc = month_date.replace(day=1)
        
        # Calculate month end
        if month_start_calc.month == 12:
            month_end_calc = month_start_calc.replace(day=31)
        else:
            next_month = month_start_calc.replace(month=month_start_calc.month + 1, day=1)
            month_end_calc = next_month - timedelta(days=1)
        
        # Count issued books in this month
        issued_count = IssuedBook.objects.filter(
            issuedate__gte=month_start_calc,
            issuedate__lte=month_end_calc
        ).count()
        
        # Count returned books in this month
        returned_count = IssuedBook.objects.filter(
            return_date__gte=month_start_calc,
            return_date__lte=month_end_calc,
            returned=True
        ).count()
        
        months_data.append(month_start_calc.strftime('%b'))
        issued_trend.append(issued_count)
        returned_trend.append(returned_count)
    
    # ========== LOW STOCK BOOKS ==========
    low_stock_books = Book.objects.filter(
        quantity__lt=3
    ).order_by('quantity')[:10]
    
    # ========== CATEGORY DISTRIBUTION ==========
    # Get category counts
    category_queryset = Book.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')[:7]
    
    # Convert to list of dicts for JSON serialization
    category_distribution = []
    for item in category_queryset:
        category_distribution.append({
            'category': item['category'] if item['category'] else 'Uncategorized',
            'count': item['count']
        })
    
    # ========== CONTEXT DATA ==========
    context = {
        # Basic stats
        'total_books': total_books,
        'available_books': available_books_count,
        'issued_books': issued_books_count,
        'total_members': total_members,
        'overdue_books': overdue_books_count,
        'books_this_month': books_this_month,
        
        # Activities and lists
        'recent_activities': recent_activities,
        'top_books': top_books,
        'low_stock_books': low_stock_books,
        
        # Chart data - JSON serialized
        'months_data': json.dumps(months_data),
        'issued_trend': json.dumps(issued_trend),
        'returned_trend': json.dumps(returned_trend),
        
        # Status breakdown for pie chart (use same variables)
        'available': available_books_count,
        'issued': issued_books_count,
        'overdue': overdue_books_count,
        
        # Category data - properly serialized
        'category_distribution': json.dumps(category_distribution),
    }
    
    return render(request, 'library/dashboard.html', context)



def adminclick_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
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


# -------------------- AFTER LOGIN --------------------

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('dashboard')
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
    # Get all books sorted by name A-Z by default
    books = Book.objects.all().order_by('name')

    # Search query
    query = request.GET.get('q', '')
    if query:
        books = books.filter(Q(name__icontains=query) | Q(author__icontains=query))

    # Apply filters using BookFilter
    book_filter = BookFilter(request.GET, queryset=books)
    books = book_filter.qs

    # Pagination (10 per page)
    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

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
            student = form.cleaned_data['student']
            book = form.cleaned_data['book']
            return_date = form.cleaned_data['return_date']
            
            # Create IssuedBook object with improved structure
            obj = models.IssuedBook()
            obj.student = student  # ForeignKey relationship
            obj.book = book        # ForeignKey relationship  
            obj.enrollment = student.enrollment
            obj.book_name = book.name
            obj.issuedate = date.today()
            obj.return_date = return_date
            obj.expirydate = return_date
            
            # Reduce book quantity
            if book.quantity > 0:
                book.quantity -= 1
                book.save()
                
                obj.save()
                # message
                messages.success(request, f'Book {book.name} issued successfully to {student.name}!')
                return render(request, 'library/bookissued.html')
            else:
                messages.error(request, "This book is out of stock!")
    
    return render(request, 'library/issuebook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    # Only show non-returned books
    issuedbooks = models.IssuedBook.objects.filter(
        returned=False
    ).select_related('student', 'book').order_by('book_name')
    
    li = []
    today = date.today()
    
    # Check if we're filtering for overdue books
    show_overdue_only = request.GET.get('show_overdue') == 'true'

    for ib in issuedbooks:
        try:
            # Get student name
            student_name = 'N/A'
            if ib.student:
                student_name = ib.student.name
            elif ib.enrollment:
                try:
                    student = models.StudentExtra.objects.get(enrollment=ib.enrollment)
                    student_name = student.name
                except models.StudentExtra.DoesNotExist:
                    student_name = 'Unknown Student'

            # Get book name - handle case where book might be deleted
            book_name = ib.book_name if ib.book_name else (ib.book.name if ib.book else 'Unknown Book')

            # Calculate fine - PKR 500 if expired
            fine = 0
            is_expired = False
            if today > ib.return_date:
                fine = 500  # PKR 500 fine
                is_expired = True

            # Only include in list if not filtering or if book is overdue
            if not show_overdue_only or is_expired:
                # Build data tuple
                li.append((
                    student_name,
                    ib.enrollment,
                    book_name,
                    ib.issuedate.strftime('%Y-%m-%d'),
                    ib.return_date.strftime('%Y-%m-%d'),
                    fine,  # Fine amount
                    is_expired,  # Flag for expired status
                    ib.id  # IssuedBook ID for return functionality
                ))

        except Exception as e:
            print(f"Error processing issued book {ib.id}: {e}")
            continue

    # Pagination (10 per page)
    paginator = Paginator(li, 10)
    page = request.GET.get('page')
    
    try:
        li_page = paginator.page(page)
    except PageNotAnInteger:
        li_page = paginator.page(1)
    except EmptyPage:
        li_page = paginator.page(paginator.num_pages)

    return render(request, 'library/viewissuedbook.html', {
        'li': li_page, 
        'show_overdue_only': show_overdue_only,
        'total_count': len(li)  # Total count for header
    }) 
    
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_issued_books_view(request):
    if request.method == "POST":
        import json
        books_data = json.loads(request.POST.get("books_data", "[]"))

        for book_data in books_data:
            issued_book = models.IssuedBook.objects.get(id=book_data["id"])
            issued_book.issue_date = book_data["issue_date"]
            issued_book.return_date = book_data["return_date"]
            issued_book.save()

        messages.success(request, "Issued books updated successfully!")
        return redirect("viewissuedbook")
    return redirect("viewissuedbook")

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def return_issued_book_view(request):
    if request.method == 'POST':
        issuedbook_id = request.GET.get('issuedbook_id')
        try:
            # Get the issued book record
            issued_book = models.IssuedBook.objects.get(id=issuedbook_id)
            
            # Get the book to increase quantity
            if issued_book.book:
                book = issued_book.book
                book.quantity += 1
                book.save()
            
            # CHANGE: Mark as returned instead of deleting
            issued_book.returned = True
            issued_book.save()
            
            messages.success(request, 'Book returned successfully!')
            
        except models.IssuedBook.DoesNotExist:
            messages.error(request, 'Issued book record not found!')
        except Exception as e:
            messages.error(request, f'Error returning book: {str(e)}')
    
    return redirect('viewissuedbook')
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
    # Get all students sorted by name A-Z by default
    students = models.StudentExtra.objects.all().order_by('name')
    
    # Search functionality
    query = request.GET.get('q', '').strip()
    if query and query != 'None':  # Handle the "None" string case
        students = students.filter(Q(name__icontains=query) | Q(enrollment__icontains=query))
    
    # Initialize filter - use StudentFilter directly
    student_filter = StudentFilter(request.GET, queryset=students)
    students = student_filter.qs

    # Pagination (10 per page)
    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

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