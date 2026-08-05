from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import Student, Address
from django.db.models import Count, Max
from .models import Department, Course, Student


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