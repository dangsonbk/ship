# Generated by Django 4.1.4 on 2023-01-29 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_vehicle_mother_laysheet_vehicle_trip'),
    ]

    operations = [
        migrations.AddField(
            model_name='laysheet',
            name='arrival_windows',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='laysheet',
            name='contract',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]