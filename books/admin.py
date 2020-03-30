from django.contrib import admin
from .models import Book,Language,History,User

class BookAdmin(admin.ModelAdmin):
    list_display = ('name','author')
    list_filter = ('name','author')
    search_fields = ('name','author')

class LanguageAdmin(admin.ModelAdmin):
    search_fields = ('name','books')

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('content_object','user')

admin.site.register(History,HistoryAdmin)
admin.site.register(User)
admin.site.register(Book,BookAdmin)
admin.site.register(Language,LanguageAdmin)