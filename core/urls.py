from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from EnerGenius_Backend.views import FirebaseLoginView, UserProfileView
from core.views_upload import UploadExcelView
from . import views
from .views import login_view, logout_view, UserUpdateView, UserCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include  
from .views_upload import UploadExcelView, PredictConsumptionView

urlpatterns = [
    path('add-item', views.add_item, name='add_item'),
    path('update-item', views.update_item, name='update_item'),
    path('delete-item', views.delete_item, name='delete_item'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("user/update/", UserUpdateView.as_view(), name="user_update"),
    # הוספת הנתיב ליצירת משתמש חדש
    path("user/create/", UserCreateView.as_view(), name="user_create"),
    path('firebase-login/', FirebaseLoginView.as_view(), name='firebase_login'),
    path('user-profile/', UserProfileView.as_view(), name='user_profile'),
    path('upload-excel/', UploadExcelView.as_view(), name='upload_excel'),
     path('upload-excel/', UploadExcelView.as_view(), name='upload_excel'),
    path('predict/', PredictConsumptionView.as_view(), name='predict_consumption'),
    
]

# הוספת קבצי מדיה ב-DEBUG MODE
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
