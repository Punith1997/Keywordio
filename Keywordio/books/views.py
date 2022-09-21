from django.shortcuts import render, redirect
from django.http import JsonResponse,  HttpResponse
from .models import Book
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login_view')
def add_book_view(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # print(request.GET)
            book_name = request.GET.get('book_name')
            author_name = request.GET.get('author_name')
            published_year = request.GET.get('published_year')
            # print(book_name, author_name, published_year)
            create_book = Book.objects.create(book_user = request.user, book_name=book_name, author_name=author_name, published_year=published_year)
            create_book.save()
            return JsonResponse({'status':'Success', 'message':'Book added successfully', 'bookid': create_book.id })
        else:
            print('not ajax request')
    return render(request, 'home.html')

@login_required(login_url='login_view')
def edit_book_view(request, book_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            book_object  = Book.objects.get(book_user = request.user, pk = book_id)
            book_name = request.GET.get('book_name')
            author_name = request.GET.get('author_name')
            published_year = request.GET.get('published_year')
            book_object.book_name = book_name
            book_object.author_name = author_name
            book_object.published_year = published_year
            book_object.save()
            return JsonResponse({'status':'Success', 'message':'Book edited successfully'})
        else:
            print('not ajax request')
    return render(request, 'home.html')

@login_required(login_url='login_view')
def delete_book_view(request, book_id = None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            book_object  = Book.objects.get(book_user = request.user, pk = book_id)
            book_object.delete()
            return JsonResponse({'status':'Success', 'message':'Book deleted successfully'})
        else:
            print('not ajax request')
    return render(request, 'home.html')
