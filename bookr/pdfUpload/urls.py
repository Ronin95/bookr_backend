from django.urls import path
from .views import PDFFileView, PDFFileListView

urlpatterns = [
    path('upload/', PDFFileView.as_view(), name='file-upload'),
    path('list/', PDFFileListView.as_view(), name='file-list'),
]
