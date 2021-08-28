from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import random

import uuid


class ProfileSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, allow_null=True,required=False)
    #is_verified = serializers.BooleanField(allow_null=True,allow_blank=True,required=False)

    class Meta:
        model = Profile
        fields = '__all__'


    def create(self, validated_data):
        user = Profile.objects.create(
            username=validated_data['username'],
            name=validated_data['name'],
            password=make_password(validated_data['password']),
            token = str(uuid.uuid4()),
            otp =  random.randint(1000,9999),
        )
        user.save()
        user.send_otp()
        user.send_verification_email()
        return user

       

class TodoSerializers(serializers.ModelSerializer):
    uname = serializers.SerializerMethodField()




    class Meta:
    
        model = Todo
        fields = "__all__"   


    def get_uname(self, obj):
        return obj.user.username


        