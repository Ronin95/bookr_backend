# pdfChat/views.py
# Importing necessary modules
from rest_framework import generics, status
from rest_framework.response import Response
from .models import TextData
from .serializers import TextDataSerializer
from django.http import JsonResponse

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