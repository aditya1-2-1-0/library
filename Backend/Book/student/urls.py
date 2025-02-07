# library/urls.py

from django import views
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path
from .views import StudentCreateAPIView,ResetPasswordAPIView,LoginAPIView,AdminSignupAPIView,IssuedBookForStudentAPIView,StudentListAPIView,OTPVerifyAPIView, BookCreateAPIView, BookListAPIView, IssuedBookCreateAPIView, IssuedBookListAPIView, IssuedBookReturnAPIView

urlpatterns = [
    path('students/create/', StudentCreateAPIView.as_view(), name='create_student'),
    path('students/', StudentListAPIView.as_view(), name='student-list'),
    path('books/', BookListAPIView.as_view(), name='list_books'),
    path('books/create/', BookCreateAPIView.as_view(), name='create_book'),
    path('issued_books/', IssuedBookCreateAPIView.as_view(), name='issue_book'),
    path('issued_books/list/', IssuedBookListAPIView.as_view(), name='list_issued_books'),
    path('issued_books/return/<int:pk>/', IssuedBookReturnAPIView.as_view(), name='return_book'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('otp-login/', OTPLoginAPIView.as_view(), name='otp-login'),
    path('otp-verify/', OTPVerifyAPIView.as_view(), name='otp-verify'),
    path('student/issued_books/', IssuedBookForStudentAPIView.as_view(), name='student-issued-books'),
    path('admin/signup/', AdminSignupAPIView.as_view(), name='admin-signup'),
    path('login/', LoginAPIView.as_view(), name='admin-login'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
]

