from django.contrib import admin
from .models import Campsite, Booking

# Класс для отображения модели Booking в админке
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'campsite', 'start_date', 'end_date', 'status')  # отображаемые поля
    list_filter = ('status',)  # фильтрация по статусу
    search_fields = ('customer_name', 'customer_email')  # поиск по имени и email

# Регистрация моделей в админке
admin.site.register(Campsite)
admin.site.register(Booking, BookingAdmin)
