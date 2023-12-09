#pdfUpload/urls.py
from django.urls import path
from .views import PDFFileView, PDFFileListView, PDFFileDeleteView, PDFFileCountView, PDFFileDetailView, SplitPDFListView, SplitPDFDetailView

urlpatterns = [
    path('upload/', PDFFileView.as_view(), name='file-upload'),
    path('list/', PDFFileListView.as_view(), name='file-list'),
    path('delete/<int:pk>/', PDFFileDeleteView.as_view(), name='file-delete'),
    path('count/', PDFFileCountView.as_view(), name='file-count'),
    path('pdf/<str:filename>/', PDFFileDetailView.as_view() ,name='pdf_file_detail'),
    path('split-pdfs/', SplitPDFListView.as_view(), name='split-pdfs-list'),
    path('split-pdfs/<str:filename>/', SplitPDFDetailView.as_view(), name='split-pdfs-detail'),
]
