from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from .views import FirebaseLoginView, UserProfileView

def home(request):
    return HttpResponse("<h1>Welcome to the Home Page</h1>")

urlpatterns = [
    path('', home, name='home'),  
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('login/', FirebaseLoginView.as_view(), name='firebase_login'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
