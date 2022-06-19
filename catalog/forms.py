from django import forms
from .models import Book, Author

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Проверка того, то дата не выходит за "верхнюю" границу (+4 недели).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Помните, что всегда надо возвращать "очищенные" данные.
        return data


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(BookCreateForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Book.objects.filter(title=title).exists():
            raise forms.ValidationError("You have already written a book with same title.")
        return title


class AuthorCreateForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ()
        unique_together = [("first_name", "last_name")]

    def __init__(self, *args, **kwargs):
        super(AuthorCreateForm, self).__init__(*args, **kwargs)


    def clean_last_name(self):
        #first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        #date_of_birth = self.cleaned_data['date_of_birth']
        if Author.objects.filter(last_name=last_name).exists():
            raise forms.ValidationError("We already have this author.")
        return last_name


