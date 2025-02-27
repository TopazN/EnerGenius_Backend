# core/views_upload.py
import pandas as pd
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import joblib

class UploadExcelView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # אפשר לבצע בדיקה שהסיומת היא xls/xlsx
        if not (file_obj.name.endswith('.xls') or file_obj.name.endswith('.xlsx')):
            return Response({"error": "File must be Excel .xls or .xlsx"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # נניח רוצים לקרוא עם pandas
            df = pd.read_excel(file_obj)
            # מעבדים את הנתונים...
            # לדוגמה: סוכמים עמודה "consumption":
            total_consumption = df['consumption'].sum()
            average_consumption = df['consumption'].mean()

            # נשמור אולי תוצאות במסד הנתונים, או נחזיר ללקוח
            return Response({
                "status": "success",
                "total_consumption": total_consumption,
                "average_consumption": average_consumption
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

MODEL_PATH = settings.BASE_DIR / "model.pkl"  # נניח ששמרנו מודל רגרסיה כלשהו
ml_model = joblib.load(MODEL_PATH)

class PredictConsumptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        צפו לפרמטרים שונים ב-POST כדי לייצר תחזית:
        """
        data = request.data
        # לדוגמה: average_daily_consumption, weekday...
        avg_consumption = float(data.get('average_daily_consumption', 0))
        weekday = int(data.get('weekday', 0))

        # מניחים שהמודל שלנו מקבל וקטור של 2 תכונות
        prediction = ml_model.predict([[avg_consumption, weekday]])
        return Response({"predicted_consumption": prediction[0]})