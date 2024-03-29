# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [
    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
    path('upload', views.document_upload, name='upload'),
    path('report', views.report, name='report'),
    path('remove', views.remove, name='remove'),
    path('download', views.download, name='download'),
]
