# pdfChat / urls.py
from django.urls import path
from .views import (TextDataListCreateAPIView, TextDataDeleteAPIView,
                    TextDataRetrieveByFilenameAPIView, TextDataUpdateAPIView,
                    split_pdf_text_view, delete_pdf, ai_answer_view)

urlpatterns = [
    path('textdata/', TextDataListCreateAPIView.as_view(), name='textdata-list-create'),
    path('textdata/<int:pk>/', TextDataDeleteAPIView.as_view(), name='textdata-delete'),
    path('textdata/<str:filename>/', TextDataRetrieveByFilenameAPIView.as_view(), name='textdata-retrieve-by-filename'),
    path('textdata/update/<int:pk>/', TextDataUpdateAPIView.as_view(), name='textdata-update'),
    path('process_pdf/<str:filename>/', split_pdf_text_view, name='process_pdf'),
    path('api/delete-pdf', delete_pdf, name='delete_pdf'),
    path('ai-answer/', ai_answer_view, name='ai_answer'),
]
