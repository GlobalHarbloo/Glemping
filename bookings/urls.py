from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.campsite_list, name='campsite_list'),
    path('campsite/<int:campsite_id>/', views.campsite_detail, name='campsite_detail'),
    path('campsite/<int:campsite_id>/book/', views.create_booking, name='create_booking'),
    path('campsite_data/', views.campsite_data, name='campsite_data'),
    path('about-us/', views.about_us, name='about_us'), 
    path('contact/', views.contact, name='contact'), 
    path('services/', views.services, name='services'), 
    path('campsite/<int:campsite_id>/<int:year>/<int:month>/', views.campsite_detail, name='campsite_detail'),
    path('filter-campsites/', views.filter_campsites, name='filter_campsites'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)