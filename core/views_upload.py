# core/views_upload.py
import pandas as pd
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import joblib
import os

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

MODEL_PATH = os.path.join(settings.BASE_DIR, "model.pkl")
ml_model = None  # TODO: Replace with trained model when available

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
    

class AnomalyDetectionView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(file_obj)  # ייתכן שתצטרכי להשתמש ב-read_excel אם זה קובץ אקסל
            df['datetime'] = pd.to_datetime(df['datetime'])
            df['consumption'] = pd.to_numeric(df['consumption'], errors='coerce')

            df.dropna(subset=['consumption'], inplace=True)

            mean = df['consumption'].mean()
            std = df['consumption'].std()

            threshold = 2  # סטיות תקן
            anomalies = df[df['consumption'] > mean + threshold * std]

            return Response({
                "status": "success",
                "anomalies_detected": len(anomalies),
                "anomalies": anomalies[['datetime', 'consumption']].head(10).to_dict(orient='records')
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AnomalyDetectionView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(file_obj)

            # המרה לזמן
            df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
            df['consumption'] = pd.to_numeric(df['consumption'], errors='coerce')

            # הסרת ערכים חסרים
            df = df.dropna(subset=['datetime', 'consumption'])

            # חישוב ממוצע וסטיית תקן
            mean = df['consumption'].mean()
            std = df['consumption'].std()

            # סינון אנומליות
            df['is_anomaly'] = ((df['consumption'] > mean + 2*std) | (df['consumption'] < mean - 2*std))
            anomalies = df[df['is_anomaly']]

            return Response({
                "status": "success",
                "anomalies_found": int(anomalies.shape[0]),
                "sample_anomalies": anomalies[['datetime', 'consumption']].head(10).to_dict(orient="records")
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
