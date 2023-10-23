# pdfUpload/models.py
from django.contrib.auth.models import User
from django.db import models

class PDFFile(models.Model):
    file = models.FileField(upload_to='uploadedPDFs/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
