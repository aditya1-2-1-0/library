from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  
    class_name = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.name



class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Available')  

    def __str__(self):
        return self.name


class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField()
    submission_date = models.DateField()
    fine_per_day = models.DecimalField(max_digits=5, decimal_places=2)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='Issued')  # Issued or Returned

    def calculate_fine(self):
        # Calculate fine only if it's overdue and the status is 'Issued'
        if self.status == 'Issued' and self.submission_date < timezone.now().date():
            days_late = (timezone.now().date() - self.submission_date).days
            if days_late > 0:
                self.fine_amount = days_late * self.fine_per_day
                self.save()  # Save only if fine is calculated



    def return_book(self):
        if self.status != 'Returned':  # Only process if not already returned
            self.status = 'Returned'
            self.calculate_fine()
            self.book.status = 'Available'
            self.book.save()
            self.save()


    def __str__(self):
        return f"{self.book.name} issued to {self.student.user.email}"


# models.py

from datetime import timedelta
from django.utils.timezone import now

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)  # Add this field

    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp}"


