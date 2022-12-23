# Generated by Django 4.1.4 on 2022-12-23 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract', models.CharField(max_length=255)),
                ('calculation', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Laytime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='parsed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='document',
            name='path',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='title',
            field=models.CharField(default='noname', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='media/'),
        ),
        migrations.CreateModel(
            name='Laysheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle', models.CharField(max_length=1000)),
                ('vehicle_mother', models.CharField(max_length=1000)),
                ('discharge_port', models.CharField(max_length=1000)),
                ('NOR_tendered', models.CharField(max_length=1000)),
                ('NOR_accepted', models.CharField(max_length=1000)),
                ('commenced_discharging', models.CharField(max_length=1000)),
                ('completed_discharging', models.CharField(max_length=1000)),
                ('cargo_quantity', models.CharField(max_length=50)),
                ('discharge_rate', models.CharField(max_length=50)),
                ('demurrage', models.CharField(max_length=50)),
                ('despatch', models.CharField(max_length=50)),
                ('laytime_allowed', models.CharField(max_length=50)),
                ('document', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.document')),
            ],
        ),
    ]