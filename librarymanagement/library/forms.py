from django import forms
from django.contrib.auth.models import User
from . import models

# -------------------- CONTACT FORM --------------------
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 30})
    )

# -------------------- ADMIN SIGNUP --------------------
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

# -------------------- BOOK FORMS --------------------
class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ['name', 'quantity', 'author', 'category', 'language']

class IssuedBookForm(forms.Form):
    quantity2 = forms.ModelChoiceField(
        queryset=models.Book.objects.all(),
        empty_label="Name and quantity",
        to_field_name="quantity",
        label='Name and quantity'
    )
    enrollment2 = forms.ModelChoiceField(
        queryset=models.StudentExtra.objects.all(),
        empty_label="Name and Enrollment",
        to_field_name='enrollment',
        label='Name and Enrollment'
    )

# -------------------- STUDENT FORMS --------------------
class AddStudentForm(forms.ModelForm):
    """Simple admin-only form to add students manually"""
    class Meta:
        model = models.StudentExtra
        fields = ['enrollment', 'branch']

class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

class StudentExtraForm(forms.ModelForm):
    class Meta:
        model = models.StudentExtra
        fields = ['enrollment', 'branch']
