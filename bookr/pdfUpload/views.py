# pdfUpload/views.py
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import PDFFile
from .serializers import PDFFileSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class PDFFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_serializer = PDFFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PDFFileListView(APIView):
    def get(self, request):
        files = PDFFile.objects.all()
        serializer = PDFFileSerializer(files, many=True)
        return Response(serializer.data)

class PDFFileDeleteView(APIView):
    def delete(self, request, pk):
        pdf_file = PDFFile.objects.get(pk=pk)
        file_path = os.path.join(settings.MEDIA_ROOT, str(pdf_file.file))
        os.remove(file_path)
        pdf_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PDFFileCountView(APIView):
    def get(self, request):
        count = PDFFile.objects.count()
        return Response({'count': count})


