# library/filters.py
import django_filters
from .models import Book, StudentExtra

class BookFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(
        field_name='category',
        choices=Book.catchoice,
        empty_label="All Categories"
    )
    language = django_filters.ChoiceFilter(
        field_name='language',
        choices=Book.langchoice,
        empty_label="All Languages"
    )

    class Meta:
        model = Book
        fields = ['category', 'language']
        
class StudentFilter(django_filters.FilterSet):
    gender = django_filters.ChoiceFilter(
        field_name='gender',
        choices=StudentExtra.genchoice,
        empty_label="Genders"
    )

    class Meta:
        model = StudentExtra
        fields = ['gender']
