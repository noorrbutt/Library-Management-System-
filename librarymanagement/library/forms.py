from django import forms
from django.contrib.auth.models import User
from . import models


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
class StudentExtraForm(forms.ModelForm):
    """Form for admin to add students manually"""
    class Meta:
        model = models.StudentExtra
        fields = ['name', 'enrollment', 'address', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control'}),
            'enrollment': forms.TextInput(attrs={'placeholder': 'Enrollment Number', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
        }