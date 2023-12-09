# pdfChat/models.py
from django.db import models

class TextData(models.Model):
    filename = models.CharField(max_length=255, null=True, blank=True)
    user_messages = models.JSONField(default=list)  # Stores messages from the user
    ai_messages = models.JSONField(default=list)  # Stores messages from the AI

    def __str__(self):
        return self.filename
