from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    # student pages
    path('', views.index, name='index'),
    path("add_book/", views.add_book, name="add_book"),
    path('view_books/', views.view_books, name='view_books'),
    path('view_students/', views.view_students, name='view_books'),
    path('issue_book/', views.issue_book, name='issue_book'),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),

    # authentication pages
    path("student_registration/", views.student_registration, name="student_registration"),
    path("change_password/", views.change_password, name="change_password"),
    path("student_login/", views.student_login, name="student_login"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("logout/", views.Logout, name="logout"),

    # deletion paths
    path("delete_book/", views.delete_book, name="delete_book"),
    path("delete_student/", views.delete_student, name="delete_student"),

]
