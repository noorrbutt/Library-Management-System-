from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class StudentExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.user.first_name} [{self.enrollment}]"

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def getuserid(self):
        return self.user.id


class Book(models.Model):
    catchoice = [
        ("Education", "Education"),
        ("Entertainment", "Entertainment"),
        ("Comics", "Comics"),
        ("Biography", "Biography"),
        ("History", "History"),
        ("Novel", "Novel"),
        ("Fiction", "Fiction"),
        ("Fantasy", "Fantasy"),
        ("Thriller", "Thriller"),
        ("Romance", "Romance"),
        ("Scifi", "Sci-Fi"),
        ("Horror", "Horror"),
        ("Poetry", "Poetry"),
        ("Children", "Children's Story"),
        ("Mystery", "Mystery"),
        ("Adventure", "Adventure"),
        ("Drama", "Drama"),
        ("Selfhelp", "Self-Help"),
        ("Religion", "Religion & Spirituality"),
        ("Technology", "Technology"),
        ("Art", "Art & Design"),
        ("Travel", "Travel"),
        ("Health", "Health & Fitness"),
    ]
    
    langchoice = [
        ("English", "English"),
        ("Urdu", "Urdu"),
    ]

    name = models.CharField(max_length=30)
    quantity = models.PositiveIntegerField()
    author = models.CharField(max_length=40)
    category = models.CharField(max_length=30, choices=catchoice, default="education")
    language = models.CharField(max_length=30, choices=langchoice, default="English")

    def __str__(self):
        return f"{self.name} [{self.quantity}]"


def get_expiry():
    return datetime.today() + timedelta(days=15)


class IssuedBook(models.Model):
    enrollment = models.CharField(max_length=30)
    quantity = models.CharField(max_length=30)
    issuedate = models.DateField(auto_now=True)
    expirydate = models.DateField(default=get_expiry)

    def __str__(self):
        return self.enrollment
