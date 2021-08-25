from rest_framework import serializers
from .models import *
import re   

from django.contrib.auth.hashers import make_password

class ProfileSerializers(serializers.ModelSerializer):



    class Meta:
        model = Profile
        fields = "__all__"


 
    

    
    def check(self,email):   
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'     
        if(re.search(regex,email)):   
            return True 
        else:           
            return False
    def validate(self, attrs):
        if not self.check(attrs['email']):
            raise serializers.ValidationError("Enter proper email")

        return attrs   




    def create(self, validated_data):
 
        passw = make_password(validated_data['password'])
        user = Profile.objects.create(username=validated_data['username'], password=passw, email=validated_data['email'],name = validated_data['name'])


        return user 

 
   

class TodoSerializers(serializers.ModelSerializer):
    uname = serializers.SerializerMethodField()




    class Meta:
    
        model = Todo
        fields = "__all__"   


    def get_uname(self, obj):
        return obj.user.username





