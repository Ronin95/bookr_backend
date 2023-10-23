# pdfUpload/views.py
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import PDFFile
from .serializers import PDFFileSerializer

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
