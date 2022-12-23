# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Document, Laysheet

# Register your models here.
admin.site.register(Document)
admin.site.register(Laysheet)