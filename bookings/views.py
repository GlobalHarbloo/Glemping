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
import requests

def send_to_telegram(message):
    url = f'https://api.telegram.org/bot8115788038:AAG4d6GY1-fSr9Y3lTPEVJpZKCaIo4s4VfA/sendMessage'
    params = {
        'chat_id': -4740428960,
        'text': message
    }
    response = requests.post(url, data=params)
    return response

def index(request):
    campsites = Campsite.objects.all()
    campsites_json = serialize('json', campsites)
    return render(request, 'bookings/index.html', {'campsites': campsites, 'campsites_json': campsites_json})


def campsite_list(request):
    # Получаем даты из параметров запроса
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

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

    # Собираем данные о забронированных датах для каждой стоянки
    booked_dates_per_campsite = {}
    for campsite in available_campsites:
        booked_dates = [
            booking.start_date.strftime('%Y-%m-%d') for booking in campsite.bookings.filter(status='confirmed')
        ]
        booked_dates_per_campsite[campsite.id] = booked_dates

    # Передаем в контекст данные
    return render(request, 'bookings/campsite_list.html', {
        'campsites': available_campsites,
        'booked_dates_per_campsite': booked_dates_per_campsite,
        'current_month_name': datetime.now().strftime('%B'),
        'year': datetime.now().year,
        'month_days': get_month_days(datetime.now()),  # добавь функцию для отображения дней месяца
    })

import calendar
from datetime import date, timedelta

from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from .models import Campsite, Booking
import calendar

def campsite_detail(request, campsite_id, year=None, month=None):
    """Подробная информация о стоянке, включая доступные даты."""

    # Устанавливаем текущую дату, если год и месяц не переданы
    today = date.today()
    year = year or today.year
    month = month or today.month

    # Получаем информацию о стоянке
    campsite = get_object_or_404(Campsite, id=campsite_id)

    # Получаем бронирования для данной стоянки
    bookings = Booking.objects.filter(campsite=campsite)

    # Преобразуем все даты бронирований в список забронированных дат
    booked_dates = [
        (booking.start_date + timedelta(days=i)).isoformat()[:10]
        for booking in bookings
        for i in range((booking.end_date - booking.start_date).days + 1)
    ]
    booked_dates = set(booked_dates)  # Преобразуем в set для быстрого поиска

    # Генерация календаря для указанного месяца и года
    cal = calendar.Calendar(firstweekday=6)  # Начинаем с воскресенья
    month_days = cal.monthdayscalendar(year, month)

    # Формируем полный список дат для месяца (YYYY-MM-DD или 0)
    month_days_all = [
        [(datetime(year, month, day).strftime('%Y-%m-%d') if day > 0 else 0) for day in week]
        for week in month_days
    ]

    # Функция для вычисления нового года и месяца и получения названия месяца
    def adjust_month(year, month, delta):
        """Утилита для вычисления нового года и месяца при переходе на delta месяцев вперед или назад"""
        new_month = (month - 1 + delta) % 12 + 1
        new_year = year + (month - 1 + delta) // 12
        return new_year, new_month, calendar.month_name[new_month]

    # Вычисляем данные для кнопок навигации на два месяца назад и два месяца вперед
    prev_month_1_year, prev_month_1, prev_month_1_name = adjust_month(year, month, -1)
    prev_month_2_year, prev_month_2, prev_month_2_name = adjust_month(year, month, -2)
    next_month_1_year, next_month_1, next_month_1_name = adjust_month(year, month, 1)
    next_month_2_year, next_month_2, next_month_2_name = adjust_month(year, month, 2)

    # Название текущего месяца
    current_month_name = calendar.month_name[month]

    # Передаем данные в шаблон
    context = {
        'campsite': campsite,
        'booked_dates': booked_dates,
        'month_days': month_days,
        'month_days_all': month_days_all,
        'month': month,
        'year': year,
        'current_month_name': current_month_name,
        'prev_month_1': {'year': prev_month_1_year, 'month': prev_month_1, 'name': prev_month_1_name},
        'prev_month_2': {'year': prev_month_2_year, 'month': prev_month_2, 'name': prev_month_2_name},
        'next_month_1': {'year': next_month_1_year, 'month': next_month_1, 'name': next_month_1_name},
        'next_month_2': {'year': next_month_2_year, 'month': next_month_2, 'name': next_month_2_name},
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
        message = f"""
        Новый запрос на бронирование:
        Имя: {customer_name}
        Email: {customer_email}
        Телефон: {customer_number}
        Дата начала: {start_date}
        Дата окончания: {end_date}
        Комментарии: {special_requests}
        Включить питание: {include_meals}
        """
        
        

        try:
            # Валидация перед сохранением
            new_booking.clean()  #  проверка пересечения дат
            new_booking.save()  # Если всё хорошо, сохраняем бронирование
            # Отправляем сообщение в Telegram
            send_to_telegram(message)
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
    return render(request, 'bookings/about_us.html')

def contact(request):
    return render(request, 'bookings/contact.html')  


def services(request):
    return render(request, 'bookings/services.html')

@csrf_exempt  # Если используете стандартный CSRF-токен, удалите эту строку
def filter_campsites(request):
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not start_date or not end_date:
            return JsonResponse({'error': 'Некорректные даты'}, status=400)

        campsites = Campsite.objects.all()
        available_campsites = []
        booked_campsites = {}

        for campsite in campsites:
            bookings = Booking.objects.filter(
                campsite=campsite,
                end_date__gte=start_date,
                start_date__lte=end_date
            )

            if bookings.exists():
                booked_dates = []
                for booking in bookings:
                    current = booking.start_date
                    while current <= booking.end_date:
                        booked_dates.append(current.strftime('%Y-%m-%d'))
                        current += timedelta(days=1)
                booked_campsites[campsite.name] = booked_dates
            else:
                available_campsites.append(campsite)

        return JsonResponse({
            'booked_campsites': booked_campsites,
            'available': [
                {
                    'id': campsite.id,
                    'name': campsite.name,
                    'image': campsite.image.url if campsite.image else '/static/images/default-image.jpg',
                    'description': campsite.description,
                }
                for campsite in available_campsites
            ]
        })

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)

def campsite_list(request):
    campsites = Campsite.objects.all()

    today = datetime.today()
    year = today.year
    month = today.month
    cal = calendar.Calendar(firstweekday=6)

    # Календарь текущего месяца
    month_days = cal.monthdayscalendar(year, month)
    month_days_all = [
        [(datetime(year, month, day).strftime('%Y-%m-%d') if day > 0 else 0) for day in week]
        for week in month_days
    ]

    # Занятые даты для всех стоянок
    booked_dates_per_campsite = {
        campsite.id: [
            (booking.start_date + timedelta(days=i)).isoformat()
            for booking in Booking.objects.filter(campsite=campsite)
            for i in range((booking.end_date - booking.start_date).days + 1)
        ]
        for campsite in campsites
    }

    current_month_name = calendar.month_name[month]

    return render(request, 'bookings/campsite_list.html', {
        'campsites': campsites,
        'month_days': month_days_all,
        'booked_dates_per_campsite': booked_dates_per_campsite,
        'year': year,
        'month': month,
        'current_month_name': current_month_name,
    })

