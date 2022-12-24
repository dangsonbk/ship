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
    laysheets = Laysheet.objects.all()
    files = documents.order_by('-uploaded_at')[:10]
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
        if ws["A1"].value and "LAYTIME CALCULATION" in ws["A1"].value:
            print("valid worksheet", ws.title)
        else:
            continue
        vehicle = ws["D2"].value
        vehicle_mother = ws["D3"].value
        discharge_port = ws["B5"].value
        NOR_tendered = ws["G5"].value
        NOR_accepted = ws["G7"].value
        commenced_discharging = ws["G9"].value
        completed_discharging = ws["G11"].value
        cargo_quantity = ws["B9"].value
        discharge_rate = ws["B11"].value
        demurrage = ws["B13"].value
        despatch = ws["B14"].value
        laytime_allowed = ws["B16"].value.strftime("%H:%M:%S")

        despatch = 0
        demurrage  = 0
        for row in ws.iter_rows(min_row=20):
            for cell in row:
                if "Despatch (USD)" in str(cell.value):
                    despatch = round(ws["G" + str(cell.row)].value or 0, 3)
                if "Demurrage (USD)" in str(cell.value):
                    demurrage = round(ws["G" + str(cell.row)].value or 0, 3)

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
            "laytime_allowed": laytime_allowed,
            "real_despatch": despatch,
            "real_demurrage": demurrage
        }

        yield results

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

    return HttpResponse("success")