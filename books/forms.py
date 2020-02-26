from django import forms
from books.models import Book,Language
from django.forms.widgets import TextInput,FileInput

'''
These are the forms. The first one is 
to create the  book and the second one 
is to update the book
The language field in CreateBooksForm is 
many-to-many field in text so that the 
user can type rather that select 
'''

class CreateBooksForm(forms.ModelForm):

    languages = forms.CharField(widget=forms.TextInput)
   
    class Meta:
        model = Book
        fields = "name","languages", "genere","about","image","book_pdf"
        

class UpdateBooksForm(forms.ModelForm):
   
    class Meta:
        model = Book
        fields = "name","language", "genere","about","image","book_pdf"