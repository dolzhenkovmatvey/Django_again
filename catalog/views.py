from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from .forms import BookCreateForm, AuthorCreateForm

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.
    num_genres = Genre.objects.count()
    num_crime_books = Book.objects.filter(title__icontains='Преступление').count() # we can paste
                                                                                # преступление
                                                                # but we are working with russian text))

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1


    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_crime_books': num_crime_books,
        'num_visits': num_visits
    }
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context=context)


from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5


class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 5

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 5


from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).order_by('due_back')


class LibrarianView(LoginRequiredMixin,PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/librarian.html'
    paginate_by = 10
    permission_required = 'catalog.can_see_all_borrowed_books'

    def get_queryset(self):
        return BookInstance.objects.all()



from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
import datetime

from .forms import RenewBookForm

@permission_required('catalog.can_see_all_borrowed_books')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            #(здесь мы просто присваиваем их полю due_back)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('all-borrowed') )

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})



from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author


class AuthorCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView,):
    model = Author
    form_class = AuthorCreateForm
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_see_all_borrowed_books'




class AuthorUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death',]
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_see_all_borrowed_books'


class AuthorDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView,):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_see_all_borrowed_books'



class BookCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_see_all_borrowed_books'
    form_class = BookCreateForm

class BookUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_see_all_borrowed_books'


class BookDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_see_all_borrowed_books'
