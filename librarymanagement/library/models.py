from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class StudentExtra(models.Model):
    genchoice = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student_profile",
    )
    name = models.CharField(max_length=30, null=True, blank=True)
    enrollment = models.CharField(max_length=40, unique=True)
    address = models.CharField(max_length=40, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=genchoice, default="Female", blank=True
    )
    photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} [{self.enrollment}]"

    @property
    def get_name(self):
        return self.name


class Book(models.Model):
    catchoice = [
        ("Education", "Education"),
        ("History", "History"),
        ("Novel", "Novel"),
        ("Fiction", "Fiction"),
        ("Thriller/Mystery", "Thriller/Mystery"),
        ("Romance", "Romance"),
        ("Scifi", "Sci-Fi"),
        ("Poetry", "Poetry"),
        ("Adventure", "Adventure"),
        ("Religion", "Religion & Spirituality"),
    ]

    langchoice = [
        ("English", "English"),
        ("Urdu", "Urdu"),
    ]

    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    author = models.CharField(max_length=40)
    category = models.CharField(max_length=30, choices=catchoice, default="Education")
    language = models.CharField(max_length=30, choices=langchoice, default="English")

    def __str__(self):
        return f"{self.name} [{self.quantity}]"


def get_expiry():
    return datetime.today() + timedelta(days=15)


class IssuedBook(models.Model):
    # Use ForeignKey for better relationships
    student = models.ForeignKey(
        StudentExtra, on_delete=models.CASCADE, null=True, blank=True
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)

    # Keep existing fields for backward compatibility
    enrollment = models.CharField(max_length=30)
    book_name = models.CharField(
        max_length=200, blank=True
    )  # Store book name separately

    issuedate = models.DateField(auto_now=True)
    expirydate = models.DateField(default=get_expiry)
    return_date = models.DateField(default=get_expiry)
    returned = models.BooleanField(default=False)  # Track if book is returned

    def __str__(self):
        return f"{self.enrollment} - {self.book_name}"

    def save(self, *args, **kwargs):
        # Auto-fill enrollment and book_name if foreign keys are provided
        if self.student and not self.enrollment:
            self.enrollment = self.student.enrollment
        if self.book and not self.book_name:
            self.book_name = self.book.name
        super().save(*args, **kwargs)


class AdminProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="admin_profile"
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="admin_photos/", null=True, blank=True)

    def __str__(self):
        return f"Profile: {self.user.username}"
