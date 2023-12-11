# pdfUpload/views.py
import os
import glob
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import PDFFile
from .serializers import PDFFileSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.http import FileResponse
from .utils import split_pdf
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator

@method_decorator(xframe_options_exempt, name='dispatch')
class PDFFileDetailView(View):
    def get(self, request, filename):
        pdf_file = get_object_or_404(PDFFile, file__icontains=filename)
        file_path = os.path.join(settings.MEDIA_ROOT, str(pdf_file.file))
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

class PDFFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_serializer = PDFFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            pdf_file_instance = file_serializer.instance

            # Construct the full file path
            file_full_path = os.path.join(settings.MEDIA_ROOT, str(pdf_file_instance.file))

            # Call split_pdf function with the correct file path
            split_pdf(file_full_path)

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
        original_file_path = os.path.join(settings.MEDIA_ROOT, str(pdf_file.file))
        os.remove(original_file_path)  # Delete the original file

        # Construct the base name to match split files
        base_name = os.path.basename(original_file_path).replace('.pdf', '')
        split_files_pattern = os.path.join(settings.MEDIA_ROOT, 'splitUpPDFs', f'{base_name}_P*.pdf')

        # Find and delete all associated split files
        for split_file in glob.glob(split_files_pattern):
            os.remove(split_file)

        pdf_file.delete()  # Delete the PDFFile record
        return Response(status=status.HTTP_204_NO_CONTENT)

class PDFFileCountView(APIView):
    def get(self, request):
        count = PDFFile.objects.count()
        return Response({'count': count})

# New view class for handling splitUpPDFs folder
class SplitPDFListView(APIView):
    def get(self, request):
        # Path to the splitUpPDFs folder
        split_pdfs_path = os.path.join(settings.MEDIA_ROOT, 'splitUpPDFs')

        # List all PDF files in the folder
        pdf_files = glob.glob(os.path.join(split_pdfs_path, '*.pdf'))
        pdf_file_names = [os.path.basename(pdf) for pdf in pdf_files]

        # Return the list of file names
        return Response(pdf_file_names)

@method_decorator(xframe_options_exempt, name='dispatch')
class SplitPDFDetailView(View):
    def get(self, request, filename):
        # Construct the full path to the requested file
        file_path = os.path.join(settings.MEDIA_ROOT, 'splitUpPDFs', filename)

        # Ensure the file exists and return it
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        else:
            return HttpResponse('File not found', status=404)
