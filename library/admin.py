from django.contrib import admin
from .models import Author, Genre, Book, Review

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'published_date')
    list_filter = ('published_date', 'genres')
    search_fields = ('title', 'author__first_name', 'author__last_name')
    date_hierarchy = 'published_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'reviewer_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('reviewer_name', 'content')