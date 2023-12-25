# pdfChat/models.py
from django.db import models

class TextData(models.Model):
    filename = models.CharField(max_length=255, null=True, blank=True)
    user_messages = models.JSONField(default=list)  # Stores messages from the user
    ai_messages = models.JSONField(default=list)  # Stores messages from the AI
    text_chunks = models.JSONField(default=list) # Stores the text chunks from the selected split up PDF
    chat_history = models.JSONField(default=list) # douple saves the input from user_messages and ai_messages

    def __str__(self):
        return self.filename
