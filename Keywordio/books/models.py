from django.db import models
from accounts.models import User

# Create your models here.
class Book(models.Model):
    book_user = models.ForeignKey(User, on_delete = models.CASCADE)
    book_name = models.CharField(max_length = 50, blank=True, null=True)
    author_name = models.CharField(max_length = 50, blank=True, null=True)
    published_year = models.CharField(max_length = 10, blank=True, null=True)

    def __str__(self):
        return "Books List"
