from django.db import models
import datetime
from django.core.exceptions import ValidationError

class Campsite(models.Model):
    name = models.CharField(max_length=100)  # Название стоянки
    description = models.TextField()         # Описание
    image = models.ImageField(upload_to='campsite_images/', blank=True, null=True)  # Поле для фото
    marker_latitude = models.FloatField(default=0.0, verbose_name="Широта маркера")
    marker_longitude = models.FloatField(default=0.0, verbose_name="Долгота маркера")

    def __str__(self):
        return self.name

    def is_available(self, start_date, end_date):
        overlapping_bookings = Booking.objects.filter(
            campsite=self,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exclude(status='pending')  # Учитываем только подтвержденные бронирования
        return not overlapping_bookings.exists()
    
    # Дополнительное поле для хранения даты последней доступности
    available_dates = models.DateField(null=True, blank=True, default=datetime.date.today)
class CampsiteImage(models.Model):
    campsite = models.ForeignKey(Campsite, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bookings/campsite_images/')  # Хранение дополнительных изображений


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждено'),
        ('paid', 'Оплачено'),
    ]
    
    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=100)
    customer_number = models.CharField(max_length=12)
    customer_email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    special_requests = models.TextField(blank=True, null=True)  # Поле для Комментариев
    
    include_meals = models.BooleanField(default=False)   # Чекбокс "Включить питание"

    def __str__(self):
        return f"Booking for {self.campsite.name} by {self.customer_name}"

    def clean(self):
        """Метод для проверки на перекрытие дат бронирования."""
        # Проверяем пересекающиеся бронирования, исключая текущую запись
        overlapping_bookings = Booking.objects.filter(
            campsite=self.campsite,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        ).exclude(pk=self.pk)
        
        if overlapping_bookings.exists():
            raise ValidationError(f"К сожалению, эти даты уже заняты для стоянки {self.campsite.name}.")
        
        # Проверка на корректность дат
        if self.start_date >= self.end_date:
            raise ValidationError("Дата окончания бронирования должна быть позже даты начала.")
        
