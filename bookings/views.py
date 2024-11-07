from django.shortcuts import render, get_object_or_404, redirect
from .models import Campsite, Booking
from django.http import HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def campsite_list(request):
    # Получаем даты из параметров запроса
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    #start_date = None
    #end_date = None
    #if not start_date or not end_date:
     #   return HttpResponseBadRequest("Пожалуйста, введите обе даты планируемого проживания")
    
    #if start_date > end_date:
     #   return HttpResponseBadRequest("Начальная дата должна быть раньше или равна конечной дате.")
    
   # if start_date < datetime.now().date():
    #    return HttpResponseBadRequest("Выбранная дата не может быть в прошлом.")
    
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Находим стоянки, у которых нет бронирований в указанный период
        available_campsites = Campsite.objects.exclude(
            bookings__start_date__lt=end_date,
            bookings__end_date__gt=start_date
        )
    else:
        # Если даты не указаны, выводим все стоянки
        available_campsites = Campsite.objects.all()
    
    return render(request, 'bookings/campsite_list.html', {'campsites': available_campsites})


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

