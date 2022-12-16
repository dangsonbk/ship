# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import template
from app.forms import UploadFileForm
from app.models import Document

@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")

@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        html_template = loader.get_template(request.path.split('/')[-1])
    except template.TemplateDoesNotExist:
        html_template = loader.get_template( 'error-404.html' )
    except:
        html_template = loader.get_template( 'error-500.html' )
    finally:
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
@csrf_exempt
def document_upload(request):
    if request.method == 'POST':
        document = request.FILES.get("file")
        title = request.POST.get("title")
        print(title)
    return render(request, 'uploaded.html')