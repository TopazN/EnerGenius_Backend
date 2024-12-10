from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse


class HelloWorldView(APIView):
    def get(self, request):  # 'self' נחוץ כאן
        return HttpResponse("Hello World!")