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
import calendar
from datetime import date, timedelta

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

import calendar
from datetime import date, timedelta

from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from .models import Campsite, Booking
import calendar

def campsite_detail(request, campsite_id):
    """Подробная информация о стоянке, включая доступные даты."""
    campsite = get_object_or_404(Campsite, id=campsite_id)

    # Получаем бронирования для данной стоянки
    bookings = Booking.objects.filter(campsite=campsite)

    # Преобразуем все даты бронирований в список забронированных дат
    booked_dates = [
        (booking.start_date + timedelta(days=i)).isoformat()[:10]  # Получаем все дни между start_date и end_date
        for booking in bookings
        for i in range((booking.end_date - booking.start_date).days + 1)
    ]
    
    # Отладка:
    print("Забронированные даты:", booked_dates)

    # Текущая дата
    today = date.today()
    year = today.year
    month = today.month

    # Получаем календарь для текущего месяца
    cal = calendar.Calendar(firstweekday=6)  # Начинаем с воскресенья
    month_days = cal.monthdayscalendar(year, month)

    # Отладка:
    print("Дни месяца:", month_days)

    # Преобразуем список забронированных дат в set для быстрого поиска
    booked_dates = set(booked_dates)

    # Создаем список полных дат для каждого дня месяца
    month_days_all = [
        [(datetime(year, month, day).strftime('%Y-%m-%d') if day > 0 else 0) for day in week]
        for week in month_days
    ]

    # Теперь передаем данные в шаблон
    context = {
        'campsite': campsite,
        'booked_dates': booked_dates,  # Список занятых дат
        'month_days': month_days,  # Список дней месяца (только числа)
        'month_days_all': month_days_all,  # Список полных дат
        'month': month,  # Текущий месяц
        'year': year,  # Текущий год
    }

    return render(request, 'bookings/campsite_detail.html', context)



@csrf_exempt
def create_booking(request, campsite_id):
    campsite = get_object_or_404(Campsite, id=campsite_id)
    
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        customer_name = request.POST.get('customer_name')
        customer_number = request.POST.get('customer_number')
        customer_email = request.POST.get('customer_email')
        special_requests = request.POST.get('special_requests', '')
        
        # Поля для чекбоксов
        include_meals = request.POST.get('include_meals') == 'on'


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
            end_date=end_date,
            special_requests=special_requests,  # необязательное текстовое поле
            include_meals=include_meals  
        )

        try:
            # Валидация перед сохранением
            new_booking.clean()  #  проверка пересечения дат
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


def about_us(request):
    return render(request, 'about_us.html')

def contact(request):
    return render(request, 'contact.html')  


def services(request):
    return render(request, 'services.html')