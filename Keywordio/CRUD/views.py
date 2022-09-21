from django.shortcuts import render
from books.models import Book

# Create your views here.
def home_view(request):
    user = request.user
    books_list = False
    if user.is_authenticated:
        books_list = Book.objects.filter(book_user=user)
    else:
        books_list = Book.objects.all()
    context = {
    'books_list':books_list,
    }
    return render(request, 'home.html', context)
