from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q 
from django.contrib import messages 
from .models import Book, Genre, Author, Review
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required

# --- BOOK MANAGEMENT ---

def manage_books(request):
    search_query = request.GET.get('search')
    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) | 
            Q(author__first_name__icontains=search_query) |
            Q(author__last_name__icontains=search_query)
        )
    else:
        books = Book.objects.all()

    if request.method == "POST":
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        price = request.POST.get('price')
        description = request.POST.get('description')
        published_date = request.POST.get('published_date')
        image = request.FILES.get('book_image')
        genre_ids = request.POST.getlist('genres')

        new_book = Book.objects.create(
            title=title,
            author_id=author_id,
            price=price,
            description=description,
            published_date=published_date,
            book_image=image
        )
        if genre_ids:
            new_book.genres.set(genre_ids)

        messages.success(request, f'"{title}" has been added!')
        return redirect('manage_books')

    authors = Author.objects.all()
    genres = Genre.objects.all()
    
    context = {
        'books': books,
        'authors': authors,
        'genres': genres,
        'search_query': search_query 
    }
    return render(request, 'library/manage_books.html', context)

def update_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == "POST":
        book.title = request.POST.get('title')
        book.description = request.POST.get('description')
        book.author_id = request.POST.get('author')
        try:
            book.price = Decimal(request.POST.get('price', '0.00'))
        except (InvalidOperation, TypeError):
            book.price = Decimal('0.00')
            
        date_str = request.POST.get('published_date')
        if date_str:
            book.published_date = date_str
            
        if request.FILES.get('book_image'):
            book.book_image = request.FILES.get('book_image')
            
        book.save()
        book.genres.set(request.POST.getlist('genres'))
        messages.success(request, f'Changes to "{book.title}" saved!')
        return redirect('manage_books')
    
    context = {
        'book': book,
        'authors': Author.objects.all(),
        'genres': Genre.objects.all(),
    }
    return render(request, 'library/update_book.html', context)

def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    title = book.title
    book.delete()
    messages.warning(request, f'"{title}" was removed.')
    return redirect('manage_books')

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == "POST":
        Review.objects.create(
            book=book,
            reviewer_name=request.POST.get('reviewer_name'),
            content=request.POST.get('content'),
            rating=request.POST.get('rating')
        )
        messages.success(request, 'Review added!')
        return redirect('book_detail', id=book.id)
    return render(request, 'library/book_detail.html', {'book': book})

# --- AUTHOR MANAGEMENT ---

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'library/author_list.html', {'authors': authors})

def author_detail(request, id):
    """View Profile Logic"""
    author = get_object_or_404(Author, id=id)
    authors_books = Book.objects.filter(author=author)
    context = {
        'author': author,
        'books': authors_books,
    }
    return render(request, 'library/author_detail.html', context)

def add_author_quick(request):
    if request.method == "POST":
        full_name = request.POST.get('name', '')
        bio = request.POST.get('bio', '')
        image = request.FILES.get('author_image')
        
        name_parts = full_name.strip().split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        Author.objects.create(
            first_name=first_name,
            last_name=last_name,
            bio=bio,
            author_image=image
        )
        messages.success(request, f'Author {full_name} added!')
        return redirect('manage_books')
    return render(request, 'library/add_author.html')

def delete_author(request, id):
    author = get_object_or_404(Author, id=id)
    name = f"{author.first_name} {author.last_name}"
    author.delete()
    messages.warning(request, f'Author "{name}" was deleted.')
    return redirect('author_list')

# --- GENRE & PROFILE ---

def add_genre_quick(request):
    if request.method == "POST":
        genre_name = request.POST.get('genre_name')
        if genre_name:
            Genre.objects.get_or_create(name=genre_name)
            messages.info(request, f'Genre "{genre_name}" added.')
        return redirect('manage_books')
    return render(request, 'library/add_genre.html')

@login_required
def profile(request):
    return render(request, 'library/profile.html', {'user': request.user})