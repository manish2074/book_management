from django.db.models.signals import m2m_changed
from .models import Book

#Every time there is change in the language of the Book, The message is sent to console saying 'Change in ManytoManyField'

def language_changed(sender,**kwargs):
    print('Change in ManytoManyField')

m2m_changed.connect(language_changed,sender=Book.language.through)    