import random
import django_filters
from django_filters import filters
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, CustomUserSerializer
from rest_framework.pagination import PageNumberPagination
import os
from typing import Dict
from ippanel import Client
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth.models import User

import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import random


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Number of products per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductFilter(django_filters.FilterSet):
    price = filters.RangeFilter()  # Filtering by price range

    class Meta:
        model = Product
        fields = ['price', 'brand', 'subcategory', 'is_promoted']  # Fields to filter by


class ProductListView(generics.ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'brand__name', 'subcategory__name']
    filterset_class = ProductFilter


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found.')

        return (user, token)


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        user = authenticate(username=phone_number, password=otp)

        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24),  # token expiry time
            'iat': datetime.utcnow(),  # issued at time
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({"token": token})




@api_view(['POST'])
def auth_request(request):
    phone_number = request.POST.get("phone_number")
    print(phone_number)
    if not phone_number:
        return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Use get_or_create with defaults to avoid race conditions
        user, created = User.objects.get_or_create(username=phone_number)

        # Generate a more secure OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # Set OTP as password
        user.set_password(otp)
        user.save()

        # Send SMS (make sure this function is implemented securely)
        send_sms(user.username, otp)

        return Response({
            "number": phone_number,
            "stage": "پیامک به شماره ی تماس ارسال شد"
        }, status=status.HTTP_200_OK)

    except Exception as e:
        # Log the exception here
        return Response({"error": f"An unexpected error occurred : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def send_sms(phone: str, otp: str) -> bool:
    # Retrieve API key from environment variable
    api_key = os.environ.get("SMS_API_KEY" , "gBGg6bUZk9ot6WNDxjlH6QYOZn0XTkgwjFM4zs0IbQ4=")
    if not api_key:
        raise ValueError("SMS API key not found in environment variables")

    # Validate phone number (basic check, can be improved)
    if not phone.isdigit() or len(phone) < 10:
        raise ValueError("Invalid phone number format")

    # Validate OTP (assuming it's a 6-digit number)
    if not otp.isdigit() or len(otp) != 6:
        raise ValueError("Invalid OTP format")

    try:
        sms = Client(api_key)
        pattern_values: Dict[str, str] = {"code": otp}

        response = sms.send_pattern(
            "cb0fl89110udnrk",  # pattern code
            "+983000505",  # originator
            phone,  # recipient
            pattern_values,  # pattern values
        )

        # Check if the SMS was sent successfully
        if response["status"] == "success":
            return True
        else:
            print(f"SMS sending failed: {response.get('message', 'Unknown error')}")
            return False

    except Exception as e:
        print(f"An error occurred while sending SMS: {str(e)}")
        return False


class ProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view!"})

class UserInfoView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.customuser


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.customuser


