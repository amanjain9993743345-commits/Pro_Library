from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default=" ") # Placeholder for old data
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    bio = models.TextField()
    author_image = models.ImageField(upload_to='authors/', default='default_author.png')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Validator added here to prevent users from selecting a date in the future
    published_date = models.DateField(
        validators=[MaxValueValidator(limit_value=date.today, message="Date cannot be in the future")]
    )
    
    book_image = models.ImageField(upload_to='books/')
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) # 1-5 Stars
    created_at = models.DateTimeField(auto_now_add=True)