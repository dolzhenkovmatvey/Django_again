# Generated by Django 4.0.5 on 2022-06-18 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_author_options_alter_book_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(default=8395568822640, help_text='13 Character <a href="https://www.isbn-international.org                            /content/what-isbn">ISBN number</a>', max_length=13, verbose_name='ISBN'),
        ),
    ]