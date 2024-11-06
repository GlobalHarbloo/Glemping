from django.db import models

class Campsite(models.Model):
    name = models.CharField(max_length=100)  # Название стоянки
    description = models.TextField()         # Описание
    location = models.CharField(max_length=100)  # Местоположение
    available_dates = models.JSONField()     # Список доступных дат

    def __str__(self):
        return self.name
    def is_available(self, start_date, end_date):
        return self.availability_start <= start_date and self.availabilty_end >= end_date

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждено'),
    ]
    
    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Booking for {self.campsite.name} by {self.customer_name}"