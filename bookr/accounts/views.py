from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import UserSerializer

@api_view(['POST'])
def register_user(request):
    data = request.data
    try:
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        return Response({"success": True, "message": "User successfully registered"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    data = request.data
    user = authenticate(username=data['username'], password=data['password'])
    if user:
        return Response({"success": True, "message": "User logged in successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"success": False, "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account_details(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
