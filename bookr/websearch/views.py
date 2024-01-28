from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WebSearch
from .serializers import WebSearchSerializer
from .utils import returnAllSearchRestults

class WebSearchView(APIView):
    def get(self, request):
        searches = WebSearch.objects.all().order_by('-id')  # Order by 'id' descending
        serializer = WebSearchSerializer(searches, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WebSearchSerializer(data=request.data)
        if serializer.is_valid():
            user_search = serializer.validated_data['user_search']

            # Call the utility function with the user search query
            exa_response, duckduckgoResult, wikiResult = returnAllSearchRestults(user_search)

            # Update the serializer with the results
            serializer.save(exa_result=exa_response, duckduckgo_result=duckduckgoResult, wikipedia_result=wikiResult)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
