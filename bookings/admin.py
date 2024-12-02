from django.contrib import admin
from django import forms
from .models import Campsite, Booking, CampsiteImage
from django.utils.safestring import mark_safe

# Класс для отображения модели Booking в админке
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'campsite', 'customer_name', 'start_date', 'end_date', 'status', 
        'special_requests', 'include_meals'
    )  # отображаемые поля
    list_filter = ('status',)  # фильтрация по статусу
    search_fields = ('customer_name', 'customer_email', 'customer_number')  # поиск по имени и email

# Регистрация модели Booking в админке
admin.site.register(Booking, BookingAdmin)  # Оставляем только эту строку регистрации

# Класс для отображения изображений в админке
class CampsiteImageInline(admin.TabularInline):
    model = CampsiteImage
    extra = 1  # Количество пустых полей для добавления изображений

# Класс формы для модели Campsite
class CampsiteAdminForm(forms.ModelForm):
    class Meta:
        model = Campsite
        fields = '__all__'

    class Media:
        js = [
            '/static/js/admin_map.js',  # путь к твоему js
        ]
        css = {
            'all': ['/static/css/admin_map.css'],  # путь к твоему css
        }

# Настройка админки
class CampsiteAdmin(admin.ModelAdmin):
    form = CampsiteAdminForm  # Подключаем кастомную форму

    list_display = ('name', 'marker_latitude', 'marker_longitude')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'image', 'marker_latitude', 'marker_longitude'),
        }),
    )
    inlines = [CampsiteImageInline]

    # Картинка маркера и карта отображаются в админке
    def render_change_form(self, request, context, *args, **kwargs):
        # Добавляем карту прямо в context
        context['adminform'].form.fields['image'].help_text = mark_safe(
            f'<div id="map-container" style="width: 100%; height: 400px; position: relative;">'
            f'<img id="camp-map-image" src="/media/camp-map.jpeg" style="width: 100%; height: 100%;">'
            f'<div id="marker" style="position: absolute; width: 20px; height: 20px; background-color: red; border-radius: 50%; cursor: pointer;"></div>'
            f'</div>'
        )
        return super().render_change_form(request, context, *args, **kwargs)

admin.site.register(Campsite, CampsiteAdmin)