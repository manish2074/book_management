from django.contrib import admin
from .models import Book,Language

class BookAdmin(admin.ModelAdmin):
    list_display = ('name','author')
    list_filter = ('name','author')
    search_fields = ('name','author')

class LanguageAdmin(admin.ModelAdmin):
    search_fields = ('name','books')
    

admin.site.register(Book,BookAdmin)
admin.site.register(Language,LanguageAdmin)