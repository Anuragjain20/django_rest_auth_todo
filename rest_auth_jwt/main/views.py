from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileSerializers,TodoSerializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
def index(request):
    return render(request, 'index.html')

class Registerapi(APIView):
    
    def post(self, request):
        try:
            prof = ProfileSerializers(data=request.data) 
          
            if not prof.is_valid():
                return Response({'error': prof.errors},status=400)                     
            username = prof.validated_data['username']
            if Profile.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'})

            prof = ProfileSerializers(data=request.data)    
            if not prof.is_valid():
                return Response({'error': prof.errors},status=400)                  
     
            prof.save()
            return Response({'message': 'User Created'})

        except Exception as e:
            print(e)
        return Response({'error': "invalid"},status=400)
class LoginView(APIView):

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = Profile.objects.filter(username=username)
            print(user)
            if user:
                user = Profile.objects.get(username=username)
                if user.check_password(password):
                    token= RefreshToken.for_user(user)
                    
                    return Response({'token': str(token),"access_token":str(token.access_token)})
                else:
                    return Response({'error': 'Invalid Credentials'})
            else:
                return Response({'error': 'Invalid Credentials'})
        except Exception as e:
            print(e)
        return Response({"error":"Unable to access"}, status=400)

class Todoview(APIView):

    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]    

    def get(self, request):
        try:
            print(request.user)
            todo = Todo.objects.filter(user=request.user)
            
            serializer = TodoSerializers(todo, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
        return Response({"error":"Unable to access"}, status=400)

    def post(self, request):
        try:
           
            request.data['user'] = request.user.id

            serializer = TodoSerializers(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=400) 
            serializer.save()
            return Response(serializer.data, status=201)
        except Exception as e:
            print(e)
        return Response({"error":"Unable to access"}, status=400)