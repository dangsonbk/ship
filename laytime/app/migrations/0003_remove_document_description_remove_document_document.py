# Generated by Django 4.1.4 on 2022-12-23 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_charge_laytime_document_parsed_document_path_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='description',
        ),
        migrations.RemoveField(
            model_name='document',
            name='document',
        ),
    ]
