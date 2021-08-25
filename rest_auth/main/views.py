from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,ProfileSerializers,TodoSerializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# Create your views here.

"""
class UserView(APIView):

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                username = serializer.data.get('username')
                password = serializer.data.get('password')
                user = User.objects.filter(username=username)
                if user:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key})
                else:
                    return Response({'error': 'Invalid Credentials'})
                 
        except Exception as e:
            print(e)

        return Response(serializer.errors, status=400)


class Todo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'todo': 'todo'})
"""
def index(request):
    return render(request, 'home.html')        

class Registerapi(APIView):
    
    def post(self, request):
        try:
            username = request.data.get('username')
            if Profile.objects.filter(username=username):
                return Response({'error': 'Username already exists'})
            request.data['password'] = make_password(request.data['password'])
            prof = ProfileSerializers(data=request.data)

     
            if prof.is_valid():
              

  
                prof.save()
                return Response({'message': 'User Created'})
            else:
                return Response({'error': 'Invalid Credentials'})
        except Exception as e:
            print(e)
        return Response(prof.errors, status=400)




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
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key})
                else:
                    return Response({'error': 'Invalid Credentials'})
            else:
                return Response({'error': 'Invalid Credentials'})
        except Exception as e:
            print(e)
        return Response({"error":"Unable to access"}, status=400)




class Todoview(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]    

    def get(self, request):
        try:
            print(request.user)
            todo = Todo.objects.filter(user=request.user)
            
            serializer = TodoSerializers(todo, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
        return Response(serializer.errors, status=400)

    def post(self, request):
        try:
            request.data['user'] = request.user.id
            serializer = TodoSerializers(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            print(e)
        return Response(serializer.errors, status=400)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]      

    def get(self, request):

        try:
            request.user.auth_token.delete()
            return Response({"message": "Successfully logged out"})
        except Exception as e:
            print(e)
        return Response({"error": "Failed to logout"}, status=400)
