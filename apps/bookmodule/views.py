from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import Student, Address
from django.db.models import Count, Max
from .models import Department, Course, Student
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import Book
from django import forms


def index(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html", {"name": name})

def index2(request, val1=0):
    return HttpResponse("value1 = " + str(val1))

def list_books(request):
    return render(request, 'bookmodule/list_books.html')

def viewbook(request, bookId):
    books = {
        123: {'id': 123, 'title': 'Continuous Delivery', 'author': 'J. Humble and D. Farley'},
        456: {'id': 456, 'title': 'Secrets of Reverse Engineering', 'author': 'E. Eilam'},
    }
    book = books.get(bookId, None)
    return render(request, 'bookmodule/show.html', {'book': book})

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')
def links(request):
    return render(request, 'bookmodule/links.html')

def formatting(request):
    return render(request, 'bookmodule/formatting.html')

def listing(request):
    return render(request, 'bookmodule/listing.html')

def tables(request):
    return render(request, 'bookmodule/tables.html')
def __getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]

def search(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword', '').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and keyword in item['title'].lower():
                contained = True
            if not contained and isAuthor and keyword in item['author'].lower():
                contained = True
            if contained:
                newBooks.append(item)
        return render(request, 'bookmodule/bookList.html', {'books': newBooks})
    return render(request, 'bookmodule/search.html')

def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def complex_query(request):
    mybooks = Book.objects.filter(author__isnull=False).filter(title__icontains='and').filter(edition__gte=2).exclude(price__lte=100)[:10]
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')

def task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/bookList.html', {'books': books})

def task2(request):
    books = Book.objects.filter(Q(edition__gt=3) & (Q(title__icontains='co') | Q(author__icontains='co')))
    return render(request, 'bookmodule/bookList.html', {'books': books})

def task3(request):
    books = Book.objects.filter(~Q(edition__gt=3) & ~(Q(title__icontains='co') | Q(author__icontains='co')))
    return render(request, 'bookmodule/bookList.html', {'books': books})

def task4(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/bookList.html', {'books': books})

def task5(request):
    stats = {
        'count': Book.objects.count(),
        'total': Book.objects.aggregate(Sum('price'))['price__sum'],
        'avg': Book.objects.aggregate(Avg('price'))['price__avg'],
        'max': Book.objects.aggregate(Max('price'))['price__max'],
        'min': Book.objects.aggregate(Min('price'))['price__min'],
    }
    return render(request, 'bookmodule/stats.html', {'stats': stats})

def task6(request):
    students = Student.objects.all()
    return render(request, 'bookmodule/students.html', {'students': students})

def task7(request):
    city_stats = Address.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/city_stats.html', {'city_stats': city_stats})

def task6(request):
    students = Student.objects.all()
    return render(request, 'bookmodule/students.html', {'students': students})

def task7(request):
    city_stats = Address.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/city_stats.html', {'city_stats': city_stats})


def lab9_task1(request):
    departments = Department.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/lab9_task1.html', {'departments': departments})

def lab9_task2(request):
    courses = Course.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/lab9_task2.html', {'courses': courses})

def lab9_task3(request):
    departments = Department.objects.annotate(oldest_student_id=Max('student__id'))
    oldest_students = []
    for dept in departments:
        student = Student.objects.filter(department=dept).order_by('id').first()
        oldest_students.append({'department': dept.name, 'student_name': student.name if student else 'None'})
    return render(request, 'bookmodule/lab9_task3.html', {'oldest_students': oldest_students})

def lab9_task4(request):
    departments = Department.objects.annotate(student_count=Count('student')).filter(student_count__gt=2).order_by('-student_count')
    return render(request, 'bookmodule/lab9_task4.html', {'departments': departments})

def list_books(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/list_books_crud.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        edition = request.POST.get('edition')
        Book.objects.create(title=title, author=author, price=price, edition=edition)
        return redirect(reverse('books.list_books'))
    return render(request, 'bookmodule/add_book.html')

def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.price = request.POST.get('price')
        book.edition = request.POST.get('edition')
        book.save()
        return redirect(reverse('books.list_books'))
    return render(request, 'bookmodule/edit_book.html', {'book': book})

def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        return redirect(reverse('books.list_books'))
    return render(request, 'bookmodule/delete_book.html', {'book': book})

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'edition']

def list_books_django(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/list_books_django.html', {'books': books})

def add_book_django(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('books.list_books_django'))
    else:
        form = BookForm()
    return render(request, 'bookmodule/add_book_django.html', {'form': form})

def edit_book_django(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect(reverse('books.list_books_django'))
    else:
        form = BookForm(instance=book)
    return render(request, 'bookmodule/edit_book_django.html', {'form': form, 'book': book})

def delete_book_django(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        return redirect(reverse('books.list_books_django'))
    return render(request, 'bookmodule/delete_book_django.html', {'book': book})