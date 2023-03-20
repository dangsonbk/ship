# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django import template
from app.models import Document, Laysheet
from app.utils import load_excel, delete_document
import os

@login_required(login_url="/login/")
def index(request):
    documents = Document.objects.all()
    laysheets = Laysheet.objects.all()
    files = documents.order_by('-uploaded_at')[:20]
    laysheetId = request.GET.get('laysheetId', '')
    if laysheetId:
        laysheets = Laysheet.objects.filter(document=int(laysheetId))
    context = {
        "file_count": documents.count(),
        "laysheets_count": laysheets.count(),
        "current_laysheets": laysheets,
        "files": files
    }
    return render(request, "index.html", context)

@login_required(login_url="/login/")
def report(request):
    laysheetId = request.GET.get('laysheetId', '')
    documents = Document.objects.all().values("id", "title")[:30]
    if laysheetId:
        document = Document.objects.get(pk=int(laysheetId))
        laysheets = Laysheet.objects.filter(document=int(laysheetId))
    else:
        document = Document.objects.last()
        laysheets = Laysheet.objects.filter(document=document)
    context = {
        "documents": documents,
        "laysheets_info": document.title,
        "current_laysheets": laysheets
    }
    return render(request, "report.html", context)

@login_required(login_url="/login/")
def remove(request):
    laysheetId = request.GET.get('laysheetId', '')
    if laysheetId:
        document = Document.objects.get(pk=int(laysheetId))
        file_path = os.path.join(settings.MEDIA_ROOT, document.path)
        delete_document(file_path)
        document.delete()
    return redirect("/")

@login_required(login_url="/login/")
def download(request):
    laysheetId = request.GET.get('laysheetId', '')
    if laysheetId:
        document = Document.objects.get(pk=int(laysheetId))
        file_path = os.path.join(settings.MEDIA_ROOT, document.path)
        print(file_path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
    return loader.get_template('error-404.html')

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
        document_title = request.POST.get("title")
        fs = FileSystemStorage()
        filename = fs.save(document_title, document)
        db_document = Document.objects.create(
            title = document_title,
            path = filename
        )
        documents_info = load_excel(fs.path(filename))
        for document_info in documents_info:
            laysheet = Laysheet.objects.create(
                document=db_document,
                **document_info
            )

    return HttpResponse({"success"}, content_type="text/plain")