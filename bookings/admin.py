from django.contrib import admin
from .models import Campsite, Booking, CampsiteImage

# Класс для отображения модели Booking в админке
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'campsite', 'start_date', 'end_date', 'status')  # отображаемые поля
    list_filter = ('status',)  # фильтрация по статусу
    search_fields = ('customer_name', 'customer_email','customer_number')  # поиск по имени и email

# Регистрация модели Booking в админке
admin.site.register(Booking, BookingAdmin)

class CampsiteImageInline(admin.TabularInline):
    model = CampsiteImage
    extra = 1  # Количество пустых полей для добавления изображений

class CampsiteAdmin(admin.ModelAdmin):
    inlines = [CampsiteImageInline]

# Регистрация модели Campsite в админке с добавлением инлайнов
admin.site.register(Campsite, CampsiteAdmin)
