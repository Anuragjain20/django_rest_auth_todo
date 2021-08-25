from rest_framework import serializers
from .models import *

class UserSerializer(serializers.Serializer):
   
    username = serializers.CharField(max_length=30)
    #email = serializers.EmailField()
    password = serializers.CharField(max_length=30)


class TodoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"   

class ProfileSerializers(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"