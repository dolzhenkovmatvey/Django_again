# Generated by Django 4.0.5 on 2022-06-18 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_bookinstance_options_alter_book_isbn'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': [('can_see_all_borrowed_books', 'View all books')]},
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(default=6942197111256, help_text='13 Character <a href="https://www.isbn-international.org                            /content/what-isbn">ISBN number</a>', max_length=13, verbose_name='ISBN'),
        ),
    ]