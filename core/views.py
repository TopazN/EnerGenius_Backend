from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
import json
from rest_framework.permissions import IsAuthenticated


User = get_user_model()  # שימוש במודל המותאם אישית

@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            full_name = data.get("full_name")

            if not email or not password or not full_name:
                return JsonResponse({"status": "error", "message": "Missing fields"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"status": "error", "message": "User already exists"}, status=400)

            user = User.objects.create_user(email=email, password=password, full_name=full_name)
            return JsonResponse({"status": "success", "message": f"User {email} added"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
def update_item(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            new_data = data.get("new_data")

            # מציאת המשתמש לפי אימייל
            user = User.objects.get(email=email)

            # עדכון השדות
            user.email = new_data.get("email", user.email)
            if "password" in new_data:
                user.set_password(new_data["password"])
            user.full_name = new_data.get("full_name", user.full_name)
            user.save()

            return JsonResponse({"status": "success", "message": f"User updated: {user.full_name}"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
def delete_item(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            email = data.get("email")

            # בדיקת אימייל
            if not email:
                return JsonResponse({"status": "error", "message": "Email is required"}, status=400)

            # בדיקה אם האימייל קיים
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"status": "error", "message": "User not found"}, status=404)

            # מחיקת המשתמש
            user.delete()
            return JsonResponse({"status": "success", "message": f"User {email} deleted"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"status": "error", "message": "Missing fields"}, status=400)

            user = authenticate(username=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({"status": "success", "message": "Login successful"})

            return JsonResponse({"status": "error", "message": "Invalid credentials"}, status=401)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"status": "success", "message": "Logout successful"})

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # מחזיר את המשתמש המחובר


class UserCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "error", "message": serializer.errors}, status=400)