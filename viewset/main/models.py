from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache
# Create your models here.



class Profile(User):

    name = models.CharField(max_length=255)
    token = models.CharField(max_length=255,blank = True, null = True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=255,blank = True, null = True)
    is_otp_verified = models.BooleanField(default=False)

    def send_otp(self):
        try:
            if not self.is_verified:
                print('sending email')
             

                subject = 'Your accounts need to be verified'
                message = f'Hi open the link and enter the number below to verify your account  http://127.0.0.1:8000/accounts/otp_verification/?email={self.username} \n {self.otp} '
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [self.username]
                cache.set(self.otp, self.username,timeout = 120*60)
                send_mail(subject, message , email_from ,recipient_list )            
    
                self.save()
        except Exception as e:
            print(e)              
            

   

    def send_verification_email(self):

        try:
            if not self.is_verified:
                print('sending email')
             

                subject = 'Your accounts need to be verified'
                message = f'Hi paste the link to verify your account http://127.0.0.1:8000/accounts/{self.token}/verified/'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [self.username]
                cache.set(self.token, self.username,timeout = 120*60)
                send_mail(subject, message , email_from ,recipient_list )            
    
                self.save()
        except Exception as e:
            print(e)    


    def __str__(self):
        return self.name


class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
   
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(Profile ,on_delete=models.CASCADE,related_name='todos')
    def __str__(self):
        return self.title

