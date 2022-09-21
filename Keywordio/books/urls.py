from django.urls import path
from . import views

urlpatterns = [
    path('add_book/', views.add_book_view, name="add_book_view"),
    path('edit_book/<int:book_id>/', views.edit_book_view, name="edit_book_view"),
    path('delete_book/<int:book_id>/', views.delete_book_view, name="delete_book_view"),
]
