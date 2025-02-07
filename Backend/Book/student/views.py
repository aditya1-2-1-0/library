
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Student, Book, IssuedBook
from .serializer import StudentSerializer, BookSerializer, IssuedBookSerializer
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password

# class StudentCreateAPIView(APIView):
#     def post(self, request):
#         data = request.data
        
#         if User.objects.filter(email=data['user']['email']).exists():
#             return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
#         user = User.objects.create_user(
#             username=data['user']['email'],  
#             email=data['user']['email'],
#             password=data['user']['password'] 
#         )
        
#         student = Student.objects.create(
#             user=user,
#             name=data['name'], 
#             class_name=data['class_name'],
#             roll_no=data['roll_no'],
#             phone_number=data['phone_number']
#         )

#         uid = urlsafe_base64_encode(str(student.user.pk).encode())
#         token = default_token_generator.make_token(student.user)

#         reset_url = f"http://127.0.0.1:8000/reset/{uid}/{token}/" 
#         print('reset_url', reset_url)

#         subject = 'Welcome to Our Service'
#         message = f'Hello {student.name},\n\nThank you for registering with us!\n\nTo set up your password, please visit the following link:\n{reset_url}'
        
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [student.user.email]  

#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#         print("sent")

#         serializer = StudentSerializer(student)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

from django.conf import settings

class StudentCreateAPIView(APIView):
    def post(self, request):
        data = request.data
        
        # Check if the email already exists
        if User.objects.filter(email=data['user']['email']).exists():
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Password validation: Make sure it's at least 6 characters long (can be extended to other criteria)
        password = data['user']['password']
        if len(password) < 6:
            return Response({'error': 'Password must be at least 6 characters long.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Create the user
            user = User.objects.create_user(
                username=data['user']['email'],
                email=data['user']['email'],
                password=password
            )
            
            # Create the student record
            student = Student.objects.create(
                user=user,
                name=data['name'],
                class_name=data['class_name'],
                roll_no=data['roll_no'],
                phone_number=data['phone_number']
            )

            # Generate token and UID for password reset
            uid = urlsafe_base64_encode(str(student.user.pk).encode())
            token = default_token_generator.make_token(student.user)
            
            # Construct the frontend password reset URL
            reset_url = f"http://localhost:4200/reset-password/{uid}/{token}"  # This will be your Angular app's route

            subject = 'Welcome to Our Service'
            message = f'Hello {student.name},\n\nThank you for registering with us!\n\nTo set up your password, please visit the following link:\n{reset_url}'

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [student.user.email]
            
            try:
                # Send the email
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                print("Email sent successfully")
            except Exception as e:
                return Response({'error': 'Failed to send email. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Return the student data after successful creation
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({'error': f"Invalid data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Catch any unforeseen errors
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class StudentListAPIView(APIView):
    def get(self, request):
       
        students = Student.objects.all()
        
        serializer = StudentSerializer(students, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookCreateAPIView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = Book.objects.create(
                name=request.data['name'],
                author=request.data['author'],
                subject=request.data['subject'],
                description=request.data['description'],
                price=request.data['price']
            )
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        return Response(BookSerializer(books, many=True).data)

# class IssuedBookListAPIView(APIView):
#     def get(self, request):
#         issued_books = IssuedBook.objects.all()
#         return Response(IssuedBookSerializer(issued_books, many=True).data)

class IssuedBookListAPIView(APIView):
    def get(self, request):
        issued_books = IssuedBook.objects.all()
        # Serialize the data with the new fields
        serialized_data = IssuedBookSerializer(issued_books, many=True)
        return Response(serialized_data.data)


class IssuedBookReturnAPIView(APIView):
    def put(self, request, pk):
        try:
            issued_book = IssuedBook.objects.get(id=pk)
            issued_book.return_book()  
            return Response(IssuedBookSerializer(issued_book).data, status=status.HTTP_200_OK)
        except IssuedBook.DoesNotExist:
            return Response({"error": "Issued book not found."}, status=status.HTTP_404_NOT_FOUND)

from django.contrib.auth.views import PasswordResetConfirmView

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = '/login/'  


class IssuedBookCreateAPIView(APIView):
    def post(self, request):
        book = Book.objects.filter(id=request.data['book']).first()
        student = Student.objects.filter(id=request.data['student']).first()

        if not book:
            raise ValidationError("The book does not exist.")
        
        if not student:
            raise ValidationError("The student does not exist.")
        
        if book.status == 'Available':
            serializer = IssuedBookSerializer(data=request.data)
            if serializer.is_valid():
                issued_book = IssuedBook.objects.create(
                    student=student,
                    book=book,
                    issue_date=request.data['issue_date'],
                    submission_date=request.data['submission_date'],
                    fine_per_day=request.data['fine_per_day']
                )
                book.status = 'Issued'
                book.save()

                return Response(IssuedBookSerializer(issued_book).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Book is already issued."}, status=status.HTTP_400_BAD_REQUEST)


from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
from .models import OTP
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from .models import OTP
from rest_framework.authtoken.models import Token
from django.conf import settings

# class LoginAPIView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         try:
#             user = User.objects.get(email=email)

#             if user.check_password(password):
#                 if user.is_staff:  # Admin login
#                     token, created = Token.objects.get_or_create(user=user)
#                     return Response({
#                         'token': token.key,
#                         'user': {
#                             'id': user.id,
#                             'email': user.email,
#                             'is_staff': user.is_staff,
#                             'is_superuser': user.is_superuser
#                         }
#                     }, status=status.HTTP_200_OK)
                
#                 else:  # Student login (OTP authentication)
#                     otp = get_random_string(length=6, allowed_chars='0123456789')
#                     otp_instance = OTP.objects.create(user=user, otp=otp, expires_at=timezone.now() + timedelta(minutes=5))

#                     # Send OTP via email
#                     subject = "Your OTP for Login"
#                     message = f"Your OTP for login is: {otp}. It expires in 5 minutes."
#                     from_email = settings.EMAIL_HOST_USER
#                     recipient_list = [user.email]
#                     send_mail(subject, message, from_email, recipient_list, fail_silently=False)

#                     # Return email and status to frontend to store email in localStorage
#                     return Response({
#                         "message": "OTP sent to your email.",
#                         "user": {
#                             "email": user.email
#                         }
#                     }, status=status.HTTP_200_OK)

#             else:
#                 return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework_simplejwt.tokens import RefreshToken
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)

            if user.check_password(password):
                if user.is_staff:  # Admin login
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': {
                            'id': user.id,
                            'email': user.email,
                            'is_staff': user.is_staff,
                            'is_superuser': user.is_superuser
                        }
                    }, status=status.HTTP_200_OK)
                
                else:  # Student login (OTP authentication)
                    otp = get_random_string(length=6, allowed_chars='0123456789')
                    otp_instance = OTP.objects.create(user=user, otp=otp, expires_at=timezone.now() + timedelta(minutes=5))

                    # Send OTP via email
                    subject = "Your OTP for Login"
                    message = f"Your OTP for login is: {otp}. It expires in 5 minutes."
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [user.email]
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                    # Return email and status to frontend to store email in localStorage
                    return Response({
                        "message": "OTP sent to your email.",
                        "user": {
                            "email": user.email
                        }
                    }, status=status.HTTP_200_OK)

            else:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import OTP, User

from rest_framework_simplejwt.tokens import RefreshToken

class OTPVerifyAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(email=email)
            otp_instance = OTP.objects.filter(user=user, otp=otp, is_verified=False).first()

            if otp_instance:
                # Check if OTP has expired (valid for 10 minutes)
                if (timezone.now() - otp_instance.created_at).total_seconds() < 600:
                    otp_instance.is_verified = True
                    otp_instance.save()

                    # Generate JWT token
                    refresh = RefreshToken.for_user(user)  # Create the refresh token
                    access_token = refresh.access_token  # Get the access token

                    return Response({
                        'message': "OTP verified successfully",
                        'token': str(access_token),  # Send the access token in the response
                        'user': {
                            'id': user.id,
                            'email': user.email,
                            'is_staff': user.is_staff,
                            'is_superuser': user.is_superuser
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
class IssuedBookForStudentAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # Specify JWT authentication
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def get(self, request):
        # Debugging: Print user to check if the user is authenticated
        print(f"Authenticated user: {request.user}")

        if request.user.is_authenticated:
            try:
                student = request.user.student
            except AttributeError:
                return Response({"error": "No student record found for this user."}, status=400)

            issued_books = IssuedBook.objects.filter(student=student)
            for issued_book in issued_books:
                issued_book.calculate_fine()

            serializer = IssuedBookSerializer(issued_books, many=True)
            return Response(serializer.data)

        return Response({"error": "Authentication credentials were not provided."}, status=401)



from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import IssuedBook
from django.conf import settings

@shared_task
def send_reminder_emails():
    tomorrow = timezone.now().date() + timezone.timedelta(days=1)
    books_to_remind = IssuedBook.objects.filter(submission_date=tomorrow, status='Issued')

    for issued_book in books_to_remind:
        student = issued_book.student
        subject = "Reminder: Book Submission Deadline"
        message = f"Dear {student.name},\n\nThis is a reminder that your book '{issued_book.book.name}' is due tomorrow.\nPlease ensure to submit it on time to avoid any fines."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [student.user.email], fail_silently=False)




class AdminSignupAPIView(APIView):
    def post(self, request):
        data = request.data
        
        if User.objects.filter(email=data['email']).exists():
            return Response({'error': 'Admin with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create(
            username=data['email'],
            email=data['email'],
            password=make_password(data['password']),  
            is_staff=True,  
            is_superuser=True  
        )
        
        return Response({'message': 'Admin created successfully.'}, status=status.HTTP_201_CREATED)
    
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status   
# class AdminLoginAPIView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         # Authenticate admin user using custom backend
#         user = authenticate(request, username=email, password=password)  # username is email in this case

#         if user and user.is_staff:  # Check if the user is an admin
#             token, created = Token.objects.get_or_create(user=user)  # Get or create a token
#             return Response({
#                 'token': token.key,
#                 'user': {
#                     'id': user.id,
#                     'email': user.email,
#                     'is_staff': user.is_staff,
#                     'is_superuser': user.is_superuser
#                 }
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials or not an admin.'}, status=status.HTTP_400_BAD_REQUEST)

# views.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = get_user_model().objects.get(email=username)  # Use email instead of username
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None


# views.py (in your Django app)
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import password_validation
from rest_framework.exceptions import ValidationError

class ResetPasswordAPIView(APIView):
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError("Invalid token or user")

        if default_token_generator.check_token(user, token):
            try:
                password_validation.validate_password(password, user)
                user.set_password(password)
                user.save()
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
