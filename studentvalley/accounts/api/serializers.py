from djoser.serializers import UserCreateSerializer , UserCreateMixin
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate 
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from accounts.models import *
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from accounts.utils import Util
import random

# User Serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email' , 
                  'image', 'numero_telephone' , 
                  'etablissement', 'first_name', 
                  'last_name' , )


# Register Serializer
class RegisterEtudinatSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)    
    class Meta: 
     model = Etudiant
     fields = ('email' , 'password' , 'specialité' , 
                  'niveau' , 'num_inscription', 
                  'image', 'numero_telephone' , 
                   'first_name', 
                  'last_name' , 'etablissement', 'faculté' ,'departement' )
       
        

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        user =Etudiant.objects.create(
                   specialité=validated_data['specialité'],
                   email=validated_data['email'],
                   password=hashed_password,
                   niveau=validated_data['niveau'],
                   num_inscription=validated_data['num_inscription'],
                   etablissement=validated_data['etablissement'],
                   first_name=validated_data['first_name'],
                   last_name=validated_data['last_name'],
                   faculté = validated_data['faculté'],
                   departement = validated_data['departement'],
                   numero_telephone = validated_data['numero_telephone'],
                   
                   
                   )

        return user
      

class ParamétreEnseignantSerializer(serializers.ModelSerializer):
      class Meta:
        model = Enseignant
        fields = ( 'image','first_name', 'last_name' , 'email', 'numero_telephone','grade',  'etablissement' , 'role')
      
        
class ParamétreEtudiantSerializer(serializers.ModelSerializer):
      class Meta:
        model = Etudiant
        fields = ( 'image','first_name', 'last_name' , 'email', 'numero_telephone','num_inscription',  'etablissement', 'faculté','departement','specialité', 
                  'niveau' ,'role' )
    
    
class ParamétreUserSerializer(serializers.ModelSerializer):
      class Meta:
        model = MyUser
        fields = ( 'email', 'first_name', 'last_name', 'numero_telephone' , 'image' , 'etablissement' , 'role')


class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']


class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  email = serializers.EmailField()
  class Meta:
    fields = ['password', 'password2']
    read_only_fields = ['email']

  def validate(self, attrs):
      password = attrs.get('password')
      password2 = attrs.get('password2')
      email = attrs.get('email')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      user = MyUser.objects.get(email=email)
      user.set_password(password)
      user.save()
      return attrs
    
  


class UpdateProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['image']
        


################################################################################################################################################################


class RegistrationInvitéSerializer (serializers.ModelSerializer):
  password = serializers.CharField(style={"input_type": "password"}, write_only=True)    

  class Meta:
    model = MyUser
    fields = ['first_name', 'last_name', 'email', 'password', 'numero_telephone']
    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        return super.create(self, validated_data)