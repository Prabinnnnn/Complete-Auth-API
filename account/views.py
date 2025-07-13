from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework.renderers import JSONRenderer
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
# Create your views here.

#this is generating tokens manually
def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer, JSONRenderer]
    def post(self, request, format=None):
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)

    
class UserLoginView(APIView):
     renderer_classes = [UserRenderer, JSONRenderer]
     def post(self, request, format=None):
          print("login endpoint hit")
          serializer = UserLoginSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          email = serializer.validated_data['email']
          password = serializer.validated_data['password']
          user = authenticate(request, email = email, password=password)
          if user is not None:
               token = get_tokens_for_user(user)
               return Response({'token': token, 'msg': 'Login Successful'}, status=status.HTTP_200_OK)
          else:
               return Response({'errors':{'non_field_errors':['Email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
               
class UserProfileView(APIView):
     renderer_classes = [UserRenderer, JSONRenderer]
     permission_classes = [IsAuthenticated]  # Ensure the user is authenticated to access this view
     def get(self, request, format=None):
          serializers = UserProfileSerializer(request.user)
          return Response(serializers.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
     renderer_classes = [UserRenderer, JSONRenderer]
     permission_classes = [IsAuthenticated]
     def post(self, request, format=None):
          serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
          if serializer.is_valid(raise_exception=True):
               return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
class SendPasswordResetEmailView(APIView):
     renderer_classes = [UserRenderer, JSONRenderer]
     def post(self, request, format=None):
          serializer = SendPasswordResetEmailSerializer(data=request.data)
          if serializer.is_valid(raise_exception=True):
               return Response({'msg': 'Password reset email sent successfully'}, status=status.HTTP_200_OK)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
     renderer_classes = [UserRenderer, JSONRenderer]
     def post(self, request, uid, token, format=None):
          serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token':token})
          if serializer.is_valid(raise_exception=True):
               return Response({'msg': 'Password reset successfully'}, status=status.HTTP_200_OK)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)