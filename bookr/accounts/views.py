# accounts/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def register_user(request):
    """
    Handle user registration.

    This view handles POST requests for user registration. It expects
    a username, email, and password in the request data. After successful
    registration, it creates a new JWT token for the user and returns it
    alongside a success message. If registration fails, it returns an error message.

    Args:
        request: The HttpRequest object containing user data for registration.

    Returns:
        Response: A Response object containing the registration status, a
        message, and a JWT token (if registration is successful).
    """

    # Extracting data from the request
    data = request.data

    try:
        # Create a new user with the provided username, email, and password
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])

        # Store the user's ID in the session for future reference
        request.session['user_id'] = user.id

        # Generate a new JWT token for the registered user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return a success response with the generated JWT token
        return Response({
            "success": True,
            "message": "User successfully registered",
            "token": access_token
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Handle any exceptions during registration and return an error response
        return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    """
    Handle user login.

    This view manages the login process. It authenticates the user with a username
    and password found in the request data. If authentication is successful, the function
    generates and returns JWT access and refresh tokens. In case of failure, it returns
    an error message indicating invalid credentials.

    Args:
        request: The HttpRequest object containing the username and password for login.

    Returns:
        Response: A Response object containing the login status, access and refresh tokens
        (if authentication is successful), or an error message.
    """

    # Extracting login data from the request
    data = request.data

    # Attempt to authenticate the user with the provided username and password
    user = authenticate(username=data['username'], password=data['password'])

    if user:
        # User authenticated successfully

        # Store the user's ID in the session for future reference
        request.session['user_id'] = user.id

        # Generate JWT access and refresh tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Return a success response with the generated tokens
        return Response({
            "success": True,
            "access_token": access_token,
            "refresh_token": refresh_token
        }, status=status.HTTP_200_OK)
    else:
        # Authentication failed
        return Response({"success": False, "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Handle user logout.

    This view manages the user logout process. It clears the user's session data,
    effectively logging them out of the system. After successfully clearing the session,
    it returns a success message.

    Args:
        request: The HttpRequest object associated with the user session.

    Returns:
        Response: A Response object containing the logout status and a success message.
    """

    # Clear all data from the current session
    request.session.flush()

    # Return a success response indicating the user has been logged out
    return Response({"success": True, "message": "Logged out successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account_details(request):
    """
    Retrieve account details of the logged-in user.

    This view fetches the details of the currently authenticated user from the request
    and serializes the user data. It then returns this serialized data, which typically
    includes user-specific information such as username, email, etc., depending on the
    fields defined in the UserSerializer.

    Args:
        request: The HttpRequest object containing the user's authentication information.

    Returns:
        Response: A Response object containing the serialized data of the user.
    """

    # Get the authenticated user from the request
    user = request.user

    # Serialize the user data
    serializer = UserSerializer(user)

    # Return the serialized user data
    return Response(serializer.data)
