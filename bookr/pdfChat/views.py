# pdfChat/views.py
# Importing necessary modules
import json
from rest_framework import generics, status
from rest_framework.response import Response
from .models import TextData
from .serializers import TextDataSerializer
from django.http import JsonResponse
from .utils import get_splitUpPDF_text, get_text_chunks, fetch_pdf, ai_answer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


# Defining a class-based view for both POST and GET
class TextDataListCreateAPIView(generics.ListCreateAPIView):
    queryset = TextData.objects.all()
    serializer_class = TextDataSerializer


class TextDataDeleteAPIView(generics.DestroyAPIView):
    queryset = TextData.objects.all()
    serializer_class = TextDataSerializer

    def delete(self, request, *args, **kwargs):
        try:
            text_data_instance = self.get_object()
            self.perform_destroy(text_data_instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class TextDataRetrieveByFilenameAPIView(generics.RetrieveAPIView):
    serializer_class = TextDataSerializer

    def get_queryset(self):
        filename = self.kwargs.get('filename', None)
        if filename:
            return TextData.objects.filter(filename=filename)
        return TextData.objects.none()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset()
        if instance.exists():
            serializer = self.get_serializer(instance.first())
            return JsonResponse(serializer.data)
        return JsonResponse({'message': 'Not found'}, status=404)


class TextDataUpdateAPIView(generics.UpdateAPIView):
    queryset = TextData.objects.all()
    serializer_class = TextDataSerializer

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

@api_view(['POST'])
def split_pdf_text_view(request, filename):
    if request.method == 'POST':
        # Fetch the TextData instance based on the filename
        text_data_instance = get_object_or_404(TextData, filename=filename)

        # Implement fetch_pdf to retrieve the PDF based on filename
        selectedPDF = [fetch_pdf(filename)]

        # Execute get_splitUpPDF_text
        text = get_splitUpPDF_text(selectedPDF)

        # Execute get_text_chunks
        text_chunks = get_text_chunks(text)

        # Update the TextData instance
        text_data_instance.text_chunks = text_chunks
        text_data_instance.save()

        return Response({'message': 'Text chunks updated successfully'})

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_pdf(request):
    try:
        data = json.loads(request.body)
        filename = data.get('filename')
        item = TextData.objects.get(filename=filename)
        item.delete()
        return JsonResponse({'message': 'PDF deleted successfully'}, status=200)
    except TextData.DoesNotExist:
        return JsonResponse({'error': 'PDF not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
def ai_answer_view(request):
    text_chunks = request.data.get('text_chunks', [])
    user_input = request.data.get('user_input', '')

    # Process the text_chunks and user_input to generate a response
    ai_response = ai_answer(text_chunks, user_input)

    return Response({'ai_message': ai_response})
