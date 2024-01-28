# websearch / urls.py

from django.urls import path
from .views import WebSearchView

urlpatterns = [
    path('userSearch/', WebSearchView.as_view(), name='userSearch'),
]
