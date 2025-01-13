from django.urls import path
from . import views

urlpatterns = [
    path('api/add-item', views.add_item, name='add_item'),
]
