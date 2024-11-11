from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.campsite_list, name='campsite_list'),
    path('campsite/<int:campsite_id>/', views.campsite_detail, name='campsite_detail'),
    path('campsite/<int:campsite_id>/book/', views.create_booking, name='create_booking'),
    path('campsite_data/', views.campsite_data, name='campsite_data'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)