# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Document(models.Model):
    title = models.CharField(max_length=255, blank=False)
    path = models.CharField(max_length=1000, blank=False)
    parsed = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uploaded_at.strftime("%d-%m-%Y %H:%M:%S") + " | " + self.title

    class Meta:
        verbose_name = 'File excel'
        verbose_name_plural = 'File excel'

class Laysheet(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    vehicle = models.CharField(max_length=1000, blank=False)
    vehicle_trip = models.CharField(max_length=1000, blank=False)
    contract = models.CharField(max_length=100, blank=False)
    arrival_windows = models.CharField(max_length=50, blank=False)
    discharge_port = models.CharField(max_length=1000, blank=False)
    NOR_tendered = models.CharField(max_length=1000, blank=False)
    NOR_accepted = models.CharField(max_length=1000, blank=False)
    commenced_discharging = models.CharField(max_length=1000, blank=False)
    completed_discharging = models.CharField(max_length=1000, blank=False)
    weight = models.CharField(max_length=50, blank=False)
    load = models.CharField(max_length=50, blank=False)
    despatch = models.CharField(max_length=50, blank=False)
    demurrage = models.CharField(max_length=50, blank=False)
    laytime_allowed = models.CharField(max_length=50, blank=False)
    real_despatch = models.FloatField(default=0)
    real_demurrage = models.FloatField(default=0)

    def __str__(self):
        return str(self.document)

class Laytime(models.Model):
    laysheet = models.ForeignKey(Laysheet, on_delete=models.CASCADE)
    working_time_date = models.DateTimeField(auto_now_add=True)
    working_time_from = models.CharField(max_length=50, blank=False)
    working_time_to = models.CharField(max_length=50, blank=False)
    working_time_isCounted = models.BooleanField(default=False)
    working_time_counted_hour = models.FloatField(default=0)
    working_time_counted_min = models.FloatField(default=0)
    working_time_counted_acc = models.FloatField(default=0)
    working_time_not_counted = models.FloatField(default=0)
    detail = models.CharField(max_length=500, blank=False)

    def __str__(self):
        return str(self.laysheet)

class Charge(models.Model):
    contract = models.CharField(max_length=255, blank=False)
    calculation = models.CharField(max_length=1000)