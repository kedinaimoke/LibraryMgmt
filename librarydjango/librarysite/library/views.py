from django.shortcuts import redirect, render, HttpResponse
from library.forms import IssueBookForm
from .models import Book, IssuedBook, Student, User
from .forms import IssueBookForm
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from datetime import date
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'library/index.html')


@login_required(login_url='/admin_login')
def add_book(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        category = request.POST.get('category')

        books = Book.objects.create(name=name, author=author, isbn=isbn, category=category)
        books.save()
        alert = True
        return render(request, 'library/add_book.html', {'alert': alert})
    return render(request, 'library/add_book.html')


@login_required(login_url='/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, 'library/view_books.html', {'books': books})


@login_required(login_url='/admin_login')
def view_students(request):
    students = Student.objects.all()
    return render(request, 'library/view_students.html', {'students': students})


@login_required(login_url='/admin_login')
def issue_book(request):
    form = forms.IssueBookForm()
    if request.method == 'POST':
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.student_id = request.POST.get('name2')
            obj.isbn = request.POST.get('isbn2')
            obj.save()
            alert = True
            context = {
                'obj': obj,
                'alert': alert
            }
            return render(request, 'library/issue_book.html', context)
    return render(request, 'library/issue_book.html', {'form': form})


def view_issued_book(request):
    issued_book = IssuedBook.objects.all()
    details = []
    for i in issued_book:
        days = (date.today() - i.issued_date)
        d = days.days
        fine = 0
        if d > 14:
            day = d - 14
            fine = day * 100
        books = list(models.Book.objects.filter(isbn=i.isbn))
        students = list(models.Student.objects.filter(user=i.student_id))
        i = 0
        for l in books:
            t = (students[i].user, students[i].user_id, books[i].name, books[i].isbn, issued_book[0].expiry_date, fine)
            i = i + 1
            details.append(t)
    context = {
        'issued_book': issued_book,
        'details': details
    }
    return render(request, 'library/view_issued_book.html', context)


@login_required(login_url='/student_login')
def student_issued_books(request):
    student = Student.objects.filter(user_id=request.user.id)
    issued_books = IssuedBook.objects.filter(student_id=student[0].user_id)
    li1 = []
    li2 = []

    for i in issued_books:
        books = Book.objects.filter(isbn=i.isbn)
        for book in books:
            t = (request.user.id, request.user.get_full_name, book.name, book.author)
            li1.append(t)

        days = (date.today() - i.issued_date)
        d = days.days
        fine = 0
        if d > 15:
            day = d - 14
            fine = day * 5
        t = (issued_books[0].issued_date, issued_books[0].expiry_date, fine)
        li2.append(t)
    context = {
        'li1': li1,
        'li2': li2
    }
    return render(request, 'library/student_issued_books.html', context)


@login_required(login_url='/student_login')
def profile(request):
    return render(request, 'library/profile.html')


@login_required(login_url='/student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        branch = request.POST.get('branch')
        classroom = request.POST.get('classroom')
        roll_no = request.POST.get('roll_no')

        student.user.email = email
        student.phone = phone
        student.branch = branch
        student.classroom = classroom
        student.roll_no = roll_no

        student.user.save()
        student.save()

        alert = True
        return render(request, 'library/edit_profile.html', {'alert': alert})
    return render(request, 'library/edit_profile.html')


def student_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        branch = request.POST.get('branch')
        classroom = request.POST.get('classroom')
        roll_no = request.POST.get('roll_no')
        image = request.FILES.get('image')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            passnotmatch = True
            return render(request, 'library/student_registration.html', {'passnotmatch': passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                        last_name=last_name)
        student = Student.objects.create(user=user, phone=phone, branch=branch, classroom=classroom, roll_no=roll_no,
                                         image=image)

        alert = True
        return render(request, 'library/student_registration.html', {'alert': alert})
    return render(request, 'library/student_registration.html')


def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, 'library/change_password.html', {'alert': alert})
            else:
                current_password_wrong = True
                return render(request, 'library/change_password.html',
                              {'current_password_wrong': current_password_wrong})
        except:
            pass
    return render(request, 'library/change_password.html')


def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # image = request.POST.get('username')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You cannot proceed because you are not a student!")
            else:
                return redirect('/profile')
        else:
            alert = True
            return render(request, 'library/student_login.html', {'alert': alert})
    return render(request, 'library/student_login.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('/add_book')
            else:
                return HttpResponse("You have been denied access because you are not a user.")
        else:
            alert = True
            return render(request, 'library/admin_login.html', {'alert': alert})
    return render(request, 'library/admin_login.html')


def delete_student(request, id):
    student = Student.objects.filter(id=id)
    student.delete()
    return redirect('/view_students')


def delete_book(request, id):
    book = Book.objects.filter(id=id)
    book.delete()
    return redirect('/view_books')


def Logout(request):
    logout(request)
    return redirect('/')
