from django.db import models
import datetime
from django.core.exceptions import ValidationError

class Campsite(models.Model):
    name = models.CharField(max_length=100)  # Название стоянки
    description = models.TextField()         # Описание
    location = models.CharField(max_length=100)  # Местоположение


    def __str__(self):
        return self.name
    def is_available(self, start_date, end_date):
        return self.availability_start <= start_date and self.availabilty_end >= end_date
    available_dates = models.DateField(null=True, blank=True, default=datetime.date.today)

# class Booking(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Ожидает'),
#         ('confirmed', 'Подтверждено'),
#     ]
    
#     campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE, related_name='bookings')
#     customer_name = models.CharField(max_length=100)
#     customer_number = models.CharField(max_length=12)
#     customer_email = models.EmailField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

#     def __str__(self):
#         return f"Booking for {self.campsite.name} by {self.customer_name}"

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
            raise ValidationError(f"К сожалению, эти даты уже заняты для {self.campsite.name}.")
