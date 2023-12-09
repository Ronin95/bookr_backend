# pdfChat/serializers.py
from rest_framework import serializers
from .models import TextData

class TextDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextData
        fields = ['id', 'filename', 'user_messages', 'ai_messages']
