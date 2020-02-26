
from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LoginView,LogoutView
from .views import BookDetail,post_delete,post_update,CreateBooksView,BookCategoryView



urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('create/',CreateBooksView.as_view(),name='create_books'),
    path('<int:pk>/',BookDetail.as_view(),name='book_detail'),
    path('<str:genere>/',BookCategoryView.as_view(),name='book_category'),
    path('<int:pk>/update/',post_update,name='update_book'),
    path('<int:pk>/delete/',post_delete,name='delete_book'),
    
    
]