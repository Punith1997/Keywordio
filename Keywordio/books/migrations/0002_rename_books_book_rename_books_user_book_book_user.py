# Generated by Django 4.1.1 on 2022-09-20 07:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(old_name="Books", new_name="Book",),
        migrations.RenameField(
            model_name="book", old_name="books_user", new_name="book_user",
        ),
    ]
