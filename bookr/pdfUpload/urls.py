from django.urls import path
from .views import PDFFileView, PDFFileListView, PDFFileDeleteView, PDFFileCountView

urlpatterns = [
    path('upload/', PDFFileView.as_view(), name='file-upload'),
    path('list/', PDFFileListView.as_view(), name='file-list'),
    path('delete/<int:pk>/', PDFFileDeleteView.as_view(), name='file-delete'),
    path('count/', PDFFileCountView.as_view(), name='file-count'),
]
