from django.urls import path
from . import views
from .views import login_view, logout_view

urlpatterns = [
    path('add-item', views.add_item, name='add_item'),
    path('update-item', views.update_item, name='update_item'),
    path('delete-item', views.delete_item, name='delete_item'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
]
