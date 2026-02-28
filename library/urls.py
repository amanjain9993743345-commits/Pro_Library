from django.urls import path
from . import views

urlpatterns = [
    # Main Books Management
    path('', views.manage_books, name='manage_books'),
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('update-book/<int:id>/', views.update_book, name='update_book'),
    path('delete-book/<int:id>/', views.delete_book, name='delete_book'),

    # Quick Add Functionality
    path('add-author-quick/', views.add_author_quick, name='add_author_quick'),
    path('add-genre-quick/', views.add_genre_quick, name='add_genre_quick'),

    # Author Management
    path('authors/', views.author_list, name='author_list'),
    path('authors/delete/<int:id>/', views.delete_author, name='delete_author'),
    
    # --- FIXED AUTHOR PROFILE PATH ---
    # This matches 'def author_detail(request, id)' in your views.py
    path('authors/<int:id>/', views.author_detail, name='author_detail'),
    
    # User Profile
    path('profile/', views.profile, name='profile'),
]