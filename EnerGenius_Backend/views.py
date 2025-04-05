from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from firebase_admin import auth as firebase_auth
from django.contrib.auth import get_user_model
from core.models import EnergyConsumption
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from .serializers import UserSerializer
from django.http import JsonResponse
import pandas as pd
from .analysis import generate_consumption_analysis

User = get_user_model()


class EnergyConsumptionUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        if not file or not file.name.endswith('.xlsx'):
            return Response({"error": "Please upload a valid Excel file (.xlsx)."}, status=400)

        try:
            df = pd.read_excel(file)

            required_columns = {'date', 'consumption_kwh'}
            if not required_columns.issubset(df.columns):
                return Response({"error": "File missing required columns."}, status=400)

            records = []
            for _, row in df.iterrows():
                record = EnergyConsumption(
                    user=request.user,
                    date=pd.to_datetime(row['date']).date(),
                    consumption_kwh=float(row['consumption_kwh'])
                )
                records.append(record)

            EnergyConsumption.objects.bulk_create(records, ignore_conflicts=True)

            return Response({"message": "File uploaded successfully."}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

class FirebaseLoginView(APIView):
    def post(self, request):
        id_token = request.data.get("id_token")
        if not id_token:
            return Response({"error": "No Firebase ID token provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded = firebase_auth.verify_id_token(id_token)
            email = decoded.get('email')
            uid = decoded.get('uid')
            name = decoded.get('name', '')  # ייתכן שיש שם מלא

            if not email:
                return Response({"error": "No email found in Firebase token"}, status=status.HTTP_400_BAD_REQUEST)

            user, created = User.objects.get_or_create(email=email, defaults={"full_name": name})
            
            # מנפיקים JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                "message": "Login successful",
                "uid": uid,
                "email": email,
                "access": access_token,
                "refresh": refresh_token
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return JsonResponse(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

class ConsumptionAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        forecast = generate_consumption_analysis(request.user)
        forecast_json = forecast.to_dict(orient='records')
        return Response({"forecast": forecast_json})