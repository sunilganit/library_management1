from django import forms
from .models import Author, Category, Book, Member


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['name', 'email', 'biography']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'description']


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = [
            'title',
            'isbn',
            'author',
            'category',
            'publisher',
            'publication_year',
            'quantity',
            'available_quantity',
            'description'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = [
            'user',
            'phone',
            'address'
        ]

        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }