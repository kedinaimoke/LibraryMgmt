from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

# Create your models here.
User = get_user_model()


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} [{self.isbn}]"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    classroom = models.CharField(max_length=20)
    branch = models.CharField(max_length=20)
    roll_no = models.CharField(max_length=3, blank=True)
    phone = models.CharField(max_length=13, blank=True)
    image = models.ImageField(upload_to='profile', blank=False, null=False)

    def __str__(self):
        return f"{self.user} [ {self.branch} ] [ {self.classroom} ] [ {self.roll_no} ]"


def expiry():
    return datetime.today() + timedelta(days=14)


class IssuedBook(models.Model):
    student_id = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)

    def __str__(self):
        return self.student_id
