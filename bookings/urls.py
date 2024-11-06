from django.urls import path
from . import views

urlpatterns = [
    path('', views.campsite_list, name='campsite_list'),
    path('campsite/<int:campsite_id>/', views.campsite_detail, name='campsite_detail'),
    path('campsite/<int:campsite_id>/book/', views.create_booking, name='create_booking'),
]
