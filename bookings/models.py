from django.db import models
import datetime
from django.core.exceptions import ValidationError

class Campsite(models.Model):
    name = models.CharField(max_length=100)  # Название стоянки
    description = models.TextField()         # Описание
    image = models.ImageField(upload_to='campsite_images/', blank=True, null=True)  # поле для фото

    def __str__(self):
        return self.name

    def is_available(self, start_date, end_date):
        """Проверка доступности стоянки на выбранные даты."""
        # Проверяем, есть ли пересечение с уже существующими бронированиями
        overlapping_bookings = Booking.objects.filter(
            campsite=self,
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        
        # Если такие бронирования есть, значит, стоянка недоступна
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
    ]
    
    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=100)
    customer_number = models.CharField(max_length=12)
    customer_email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Booking for {self.campsite.name} by {self.customer_name}"

    def clean(self):
        """Метод для проверки на перекрытие дат бронирования"""
        # Проверяем, есть ли другие бронирования с этим участком и пересекаются ли даты
        overlapping_bookings = Booking.objects.filter(
            campsite=self.campsite,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        )
        
        if overlapping_bookings.exists():
            raise ValidationError(f"К сожалению, эти даты уже заняты для стоянки {self.campsite.name}.")
