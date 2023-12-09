# pdfChat / urls.py

# urls.py in your Django app

from django.urls import path
from .views import TextDataListCreateAPIView, TextDataDeleteAPIView, TextDataRetrieveByFilenameAPIView

urlpatterns = [
    path('textdata/', TextDataListCreateAPIView.as_view(), name='textdata-list-create'),
    path('textdata/<int:pk>/', TextDataDeleteAPIView.as_view(), name='textdata-delete'),
    path('textdata/<str:filename>/', TextDataRetrieveByFilenameAPIView.as_view(), name='textdata-retrieve-by-filename'),

]
