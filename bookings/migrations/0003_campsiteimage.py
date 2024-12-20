# Generated by Django 5.1.3 on 2024-11-11 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_remove_campsite_location_campsite_available_dates_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampsiteImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='bookings/campsite_images/')),
                ('campsite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='bookings.campsite')),
            ],
        ),
    ]
