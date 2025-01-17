from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
import json

User = get_user_model()  # שימוש במודל המותאם אישית

@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            full_name = data.get("full_name")

            # אימות נתונים
            if not email or not password or not full_name:
                return JsonResponse({"status": "error", "message": "Missing fields"}, status=400)
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({"status": "error", "message": "Invalid email"}, status=400)

            # שמירה ב-Database
            user = User.objects.create_user(email=email, password=password, full_name=full_name)
            return JsonResponse({"status": "success", "message": f"User added: {user.full_name}"})
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
