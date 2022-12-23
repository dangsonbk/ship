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
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    vehicle = models.CharField(max_length=1000, blank=False)
    vehicle_mother = models.CharField(max_length=1000, blank=False)
    discharge_port = models.CharField(max_length=1000, blank=False)
    NOR_tendered = models.CharField(max_length=1000, blank=False)
    NOR_accepted = models.CharField(max_length=1000, blank=False)
    commenced_discharging = models.CharField(max_length=1000, blank=False)
    completed_discharging = models.CharField(max_length=1000, blank=False)
    cargo_quantity = models.CharField(max_length=50, blank=False)
    discharge_rate = models.CharField(max_length=50, blank=False)
    demurrage = models.CharField(max_length=50, blank=False)
    despatch = models.CharField(max_length=50, blank=False)
    laytime_allowed = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return str(self.document)

class Laytime(models.Model):
    pass

class Charge(models.Model):
    contract = models.CharField(max_length=255, blank=False)
    calculation = models.CharField(max_length=1000)