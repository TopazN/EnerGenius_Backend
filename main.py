import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EnerGenius_Backend.settings')
application = get_wsgi_application()

if __name__ == "__main__":
    print("EnerGenius Backend is running!")
