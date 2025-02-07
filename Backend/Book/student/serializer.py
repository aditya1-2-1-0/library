from rest_framework import serializers
from .models import Student, Book, IssuedBook
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from rest_framework import serializers
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'name', 'class_name', 'roll_no', 'phone_number']

    def validate_roll_no(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Roll number must be alphanumeric.")
        return value


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'subject', 'description', 'price', 'status']

    def validate(self, data):
        if not data['price'] >= 0:
            raise serializers.ValidationError("Price must be greater than or equal to 0.")
        return data


from rest_framework import serializers
from .models import IssuedBook, Student, Book

class IssuedBookSerializer(serializers.ModelSerializer):
    # Include student and book details in the serializer
    student_name = serializers.CharField(source='student.name')
    book_name = serializers.CharField(source='book.name')
    book_author = serializers.CharField(source='book.author')

    class Meta:
        model = IssuedBook
        fields = ['id', 'student_name', 'book_name', 'book_author', 'issue_date', 'submission_date', 'fine_per_day']

    def validate_submission_date(self, value):
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d').date()
        
        if value <= timezone.now().date():
            raise serializers.ValidationError("Submission date must be in the future.")
        return value

    def validate_issue_date(self, value):
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d').date()

        if value >= timezone.now().date():
            raise serializers.ValidationError("Issue date cannot be in the future.")
        return value

    def validate_fine_per_day(self, value):
        if value < 0:
            raise serializers.ValidationError("Fine per day must be a positive value.")
        return value

    def create(self, validated_data):
        fine_per_day = validated_data.get('fine_per_day')
        submission_date = validated_data.get('submission_date')
        issue_date = validated_data.get('issue_date')

        overdue_days = (submission_date - issue_date).days
        fine_amount = fine_per_day * overdue_days if overdue_days > 0 else 0

        issued_book = IssuedBook.objects.create(fine_amount=fine_amount, **validated_data)
        return issued_book

from rest_framework import serializers

class OTPLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    otp = serializers.IntegerField(write_only=True)

