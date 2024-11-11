from django.shortcuts import render, get_object_or_404, redirect
from .models import Campsite, Booking
# from django.http import HttpResponse
# from django.http import HttpResponseBadRequest
# from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
from django.http import JsonResponse

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
    campsite = get_object_or_404(Campsite, id=campsite_id)
    
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        customer_name = request.POST.get('customer_name')
        customer_number = request.POST.get('customer_number')
        customer_email = request.POST.get('customer_email')

        # Проверка наличия данных
        if not (start_date_str and end_date_str and customer_name and customer_number and customer_email):
            return JsonResponse({"error": "Пожалуйста, заполните все поля."}, status=400)

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        # Создаём бронирование
        new_booking = Booking(
            campsite=campsite,
            customer_name=customer_name,
            customer_number=customer_number,
            customer_email=customer_email,
            start_date=start_date,
            end_date=end_date
        )

        try:
            # Валидация перед сохранением
            new_booking.clean()  # Вызываем метод clean для проверки пересечения дат
            new_booking.save()  # Если всё хорошо, сохраняем бронирование
            return JsonResponse({"message": "Бронирование успешно создано!"})
        except ValidationError as e:
            # Извлекаем только текст ошибки из ValidationError и возвращаем его
            error_message = " ".join(e.messages)
            return JsonResponse({"error": error_message}, status=400)

    # Возвращаем форму для бронирования, если запрос не POST
    return render(request, 'bookings/create_booking.html', {'campsite': campsite})


def campsite_data(request):
    campsites = Campsite.objects.all()
    data = []
    
    for campsite in campsites:
        data.append({
            'id': campsite.id,
            'name': campsite.name,
            'latitude': campsite.latitude,
            'longitude': campsite.longitude
        })
    
    return JsonResponse(data, safe=False)

def campsite_detail(request, campsite_id):
    campsite = get_object_or_404(Campsite, id=campsite_id)
    return render(request, 'bookings/campsite_detail.html', {'campsite': campsite})
