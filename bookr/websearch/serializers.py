from rest_framework import serializers
from .models import WebSearch

class WebSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebSearch
        fields = ['id', 'user_search', 'exa_result', 'wikipedia_result', 'duckduckgo_result']