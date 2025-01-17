from django.urls import path
from . import views

urlpatterns = [
    path('api/add-item', views.add_item, name='add_item'),
    path('api/update-item', views.update_item, name='update_item'),  # הנתיב החדש לעדכון פריטים
    path('api/delete-item', views.delete_item, name='delete_item'),  # הנתיב למחיקה
]
