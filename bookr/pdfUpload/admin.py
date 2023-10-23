# pdfUpload/admin.py
from django.contrib import admin
from .models import PDFFile

admin.site.register(PDFFile)
