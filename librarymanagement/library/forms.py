from django import forms
from django.contrib.auth.models import User
from . import models
from datetime import date, timedelta


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
    default_return_date = date.today() + timedelta(days=15)
    
    book = forms.ModelChoiceField(
        queryset=models.Book.objects.filter(quantity__gt=0),  # Only show available books
        empty_label="Select Book",
        label='Book Name',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    student = forms.ModelChoiceField(
        queryset=models.StudentExtra.objects.all(),
        empty_label="Select Student",
        label='Student',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    return_date = forms.DateField(
        initial=default_return_date,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Return Date'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the display of books to show name and availability
        self.fields['book'].label_from_instance = lambda obj: f"{obj.name} (Available: {obj.quantity})"
        # Customize the display of students to show name and enrollment
        self.fields['student'].label_from_instance = lambda obj: f"{obj.name} - {obj.enrollment}"
# -------------------- STUDENT FORMS --------------------
class StudentExtraForm(forms.ModelForm):
    """Form for admin to add students manually"""
    class Meta:
        model = models.StudentExtra
        fields = ['name', 'enrollment', 'address', 'phone', 'gender']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control'}),
            'enrollment': forms.TextInput(attrs={'placeholder': 'Enrollment Number', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_enrollment(self):
        enrollment = self.cleaned_data.get('enrollment')
        if enrollment:
            # Check if enrollment number already exists
            if models.StudentExtra.objects.filter(enrollment=enrollment).exists():
                raise forms.ValidationError("This enrollment number already exists.")
        return enrollment