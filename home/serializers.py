from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('username already exists')
            
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError('email already exists')
        
        return data 
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    


class ColorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Color
        fields = ['color_name']




class StudentSerializer(serializers.ModelSerializer):
    # color = ColorSerializer()
    # country = serializers.SerializerMethodField()
    # color_info = serializers.SerializerMethodField()

    class Meta:
        model = Student
        # fields = ['name','age']
        #exclude = ['id']
        fields = '__all__'
        # depth = 1    

    # def get_color_info(self, obj):
    #     color_obj = Color.objects.get(id = obj.color.id)
    #     return {"color_name": color_obj.color_name, "hex_code": "0010"}
        
    
    # def get_country(self, obj):
    #     return "India"
    
    # def validate(self, data):
    #     special_characters = "!@#$%^&*()-+?_=,<>/"
    #     if any(c in special_characters for c in data['name']):
    #         raise serializers.ValidationError('name cannot contain special chars')


    #     if data['age'] < 18:
    #         raise serializers.ValidationError('age should be greater than 18')
        
    #     return data

