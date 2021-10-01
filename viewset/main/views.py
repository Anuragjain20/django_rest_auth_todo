from django.shortcuts import render,HttpResponse
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.cache import cache

# Create your views here.
def test(request):
    return HttpResponse('<h1>Hello World!</h1>')

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    

    @action(methods=['get'],detail=True)
    def verified(self, request,pk):
        try:
            if not cache.get(pk):
                return Response({'status':'not verified' , 'message':'token expired'})
            print(cache.ttl(pk))

            user = Profile.objects.get(token=pk)
            user.is_verified = True
            user.save()
            return Response({'status':'success'})

        except Exception as e:
            return Response({'status':'failure'})


    @action(methods=['post'],detail=False)
    def otp_verification(self, request):
        try:
            email = request.GET.get('email')
            user = Profile.objects.get(username=email)
            print(user)

            pk = request.data["otp"]
            print(pk)
            if not cache.get(pk):
                return Response({'status':'not verified' , 'message':'token expired'})
            print(cache.ttl(pk))

           
            user.is_otp_verified = True
            user.save()
            return Response({'status':'success'})

        except Exception as e:
            return Response({'status':'failure'})            

    @action(methods=['post'],detail=False)
    def forgot_password(self,request):
        try:
            username = request.data['username']
            user = Profile.objects.get(username=username)
            user.token = str(uuid.uuid4())

            user.save()
            send_reset_email(user)
            return Response({'status':'success'})
        except Exception as e:
            return Response({'status':'failure'})

    @action(methods=['post'],detail=True)
    def reset_password(self,request,pk):
        try:
            if not cache.get(pk):
                return Response({'status':'not verified' , 'message':'token expired'})
            print(cache.ttl(pk))           
            password = request.data['password']
            user = Profile.objects.get(token=pk)
            print(user)
            user.password = make_password(str(password))
            user.save()
            return Response({'status':'success'})
        except Exception as e:
            print(e)
            return Response({'status':'failure'})

       

    @action(methods=['post'],detail=False)
    def  login_auth(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username,password=password)
            #user = Profile.objects.filter(username=username)
            print(user)
            if user:
                user = Profile.objects.get(username=username)
                if user.is_verified and user.is_otp_verified and   user.check_password(password):
                    token= RefreshToken.for_user(user)
                    
                    return Response({'token': str(token),"access_token":str(token.access_token)})
                else:
                    return Response({'error': 'Invalid Credentials'})
            else:
                return Response({'error': 'Invalid Credentials'})
        except Exception as e:
            print(e)
        return Response({"error":"Unable to access"}, status=400)
                                          

    def list(self, request, *args, **kwargs):
        if request.GET.get('search'):

            queryset = Profile.objects.filter(name__icontains = request.GET.get('search'))
        else:
            queryset = self.filter_queryset(self.get_queryset())
        serialize = self.serializer_class(queryset,many = True) 
    
        return Response({"data":serialize.data})   
 
#gte
#lte
#exclude
#icontains - not case sensistve
#iexact - case senistive



class TodoView(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = super().get_queryset() 
        data = queryset.filter(user=self.request.user)
        return data
    queryset = Todo.objects.all()    
        
    serializer_class = TodoSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 




def send_reset_email(obj):

    try:
       
        print('sending email')
            

        subject = 'Reset Password'
        message = f'Hi visit this link for reset password http://127.0.0.1:8000/accounts/{obj.token}/reset_password/'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [obj.username]
        send_mail(subject, message , email_from ,recipient_list )         
        cache.set(obj.token, obj.username,timeout = 120)   

        obj.save()
    except Exception as e:
        print(e)    
