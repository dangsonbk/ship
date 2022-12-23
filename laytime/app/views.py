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
from django import template
from app.models import Document, Laysheet
from openpyxl import load_workbook

@login_required(login_url="/login/")
def index(request):
    documents = Document.objects.all()
    files = documents.order_by('-uploaded_at')[:10]
    context = {
        "file_count": documents.count(),
        "files": files
    }
    return render(request, "index.html", context)

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

def load_excel(path):
    wb = load_workbook(path, data_only=True)
    for ws in wb:
        if "LAYTIME CALCULATION" in ws["A1"].value:
            print("valid worksheet", ws.title)
        else:
            continue
        vehicle = ws["D2"].value
        vehicle_mother = ws["D3"].value
        discharge_port = ws["B5"].value
        NOR_tendered = ws["G5"].value
        NOR_accepted = ws["G7"].value

        commenced_discharging = discharge_port = ws["G9"].value
        completed_discharging = discharge_port = ws["G11"].value
        cargo_quantity = discharge_port = ws["B9"].value
        discharge_rate = discharge_port = ws["B11"].value
        demurrage = discharge_port = ws["B13"].value
        despatch = discharge_port = ws["B14"].value
        laytime_allowed = discharge_port = ws["B16"].value

        results = {
            "vehicle": vehicle,
            "vehicle_mother": vehicle_mother,
            "discharge_port": discharge_port,
            "NOR_tendered": NOR_tendered,
            "NOR_accepted": NOR_accepted,
            "commenced_discharging": commenced_discharging,
            "completed_discharging": completed_discharging,
            "cargo_quantity": cargo_quantity,
            "discharge_rate": discharge_rate,
            "demurrage": demurrage,
            "despatch": despatch,
            "laytime_allowed": laytime_allowed
        }

        return results

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
        document_info = load_excel(fs.path(filename))
        laysheet = Laysheet.objects.create(
            document=db_document,
            **document_info
        )

    return HttpResponse("success")