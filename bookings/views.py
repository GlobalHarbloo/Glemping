from django.shortcuts import render, get_object_or_404, redirect
from .models import Campsite, Booking
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

def campsite_list(request):
    start_date = None
    end_date = None
    """Отображение всех стоянок."""
    campsites = Campsite.objects.all()
    
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            campsites = [campsite for campsite in campsites if campsite.is_available(start_date, end_date)]
            
    return render(request, 'bookings/campsite_list.html', {'campsites': campsites})


def campsite_detail(request, campsite_id):
    """Подробная информация о стоянке, включая доступные даты."""
    campsite = get_object_or_404(Campsite, id=campsite_id)
    return render(request, 'bookings/campsite_detail.html', {'campsite': campsite})


@csrf_exempt
def create_booking(request, campsite_id):
    """Создание нового бронирования."""
    campsite = get_object_or_404(Campsite, id=campsite_id)
    
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Создаём запись в базе данных
        booking = Booking(
            campsite=campsite,
            customer_name=customer_name,
            customer_email=customer_email,
            start_date=start_date,
            end_date=end_date,
            status='pending'
        )
        booking.save()
        
        return HttpResponse("Бронирование успешно создано!")
    
    return render(request, 'bookings/create_booking.html', {'campsite': campsite})
