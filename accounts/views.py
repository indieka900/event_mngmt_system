from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer

User = get_user_model()

class UserSignUpView(APIView):
    """
    View to handle user signup.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "response": 0,
                "message": "User created successfully.",
                "user": CustomUserSerializer(user).data
                }, status=status.HTTP_201_CREATED)
        return Response({
            "response": 1,
            "message": "User creation failed.",
            "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    """
    View to handle user login and return JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'response': 1,
                'message': 'Email and password are required.',
                'data' : None
                }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'response': 0,
                    'message': 'Login successful.',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': CustomUserSerializer(user).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'response': 1,
                    'message': 'Invalid credentials.',
                    'data': None
                    }, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({
                'response': 1,
                'message': 'User not found.',
                'data': None
                }, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    """
    View to handle user profile retrieval and update.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response({
            'response': 0,
            'message': 'User profile retrieved successfully.',
            'user': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'response': 0,
                'message': 'User profile updated successfully.',
                'user': CustomUserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({
            'response': 1,
            'message': 'Profile update failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)