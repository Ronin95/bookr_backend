from django.urls import path
from .views import agent_view

urlpatterns = [
    path('userInput/', agent_view, name="agent_view")
]