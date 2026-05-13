from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import Etudiant , Enseignant , MyUser
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from accounts.models import MyUser
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from accounts.utils import Util
from gestion_projet.models import *

#################################################### ETUDIANT USER ###################################################################

class ProjetDepotSerializer (serializers.ModelSerializer) :
  co_encadreur_email=serializers.EmailField()
  encadreur_email=serializers.EmailField()
     
  class Meta :
    model = Projet
    fields = ['id','co_encadreur_email', 'encadreur_email', 'file' , 'nom_société' ,'domaine_projet' , 'theme' ,  'membre1_email' , 'membre2_email' , 'membre3_email' , 'membre4_email' , 'membre5_email']
    read_only_fields = ['id', 'co_encadreur_email', 'encadreur_email']
    
  def create(self, validated_data):
        validated_data.pop('co_encadreur_email', None)  
        validated_data.pop( 'encadreur_email', None)
        return super().create(validated_data)

  def update(self, instance, validated_data):
        validated_data.pop('co_encadreur_email', None)  
        validated_data.pop( 'encadreur_email', None)
        
        return super().update(instance, validated_data)
  
class ListProjetSerializer (serializers.ModelSerializer) :
     url = serializers.HyperlinkedIdentityField(
        view_name='Projet-detail',
        read_only=True,
        lookup_field = 'pk'
      )
     class Meta :
          model = Projet
          fields = [ 'url','co_encadreur', 'encadreur', 'porteur_projet', 'file' , 'nom_société' ,'domaine_projet' , 'theme'  ]
    
    

  
      
class OwnerProjectDetailSerializer (serializers.ModelSerializer):
  latest_modification = serializers.SerializerMethodField()
  co_encadreur = serializers.StringRelatedField()
  encadreur = serializers.StringRelatedField()
  membre1 = serializers.StringRelatedField()
  membre2 = serializers.StringRelatedField()
  membre3 = serializers.StringRelatedField()
  membre4 = serializers.StringRelatedField()
  membre5 = serializers.StringRelatedField()


  
  class Meta :
    model = Projet
    fields = ['id','co_encadreur', 'encadreur', 'file', 'nom_société','domaine_projet', 'theme' ,'date_depot',  'latest_modification' , 'porteur_projet' , 'membre1' , 'membre2' , 'membre3' , 'membre4' , 'membre5']  
    
    
  def get_latest_modification(self, obj):
        latest_modification = Modification.objects.filter(projet=obj).last()
        if latest_modification:
            u =latest_modification.date_modification
            return  u
                # Add other fields from the Modification model if needed
        return None
      
class EtatProjetSerializer (serializers.Serializer):
    STATUT_CHOICES = [
        ('approuvé', 'Approuvé'),
        ('en_attente', 'En attente'),
        ('rejeté', 'Rejeté'),
      ]
    date_debut = serializers.DateField( allow_null=True  )
    date_fin = serializers.DateField( allow_null=True )
    date_depot = serializers.DateField( allow_null=True)
    derniere_modification = serializers.DateTimeField( allow_null=True )
    statut_projet = serializers.ChoiceField(choices=STATUT_CHOICES )
    commentaire = serializers.CharField( allow_null=True )
     
      
#################################################### COMITE USER ###################################################################
  
class ReviewSerializer (serializers.ModelSerializer):
  
  class Meta:
      model = Review
      fields = ['commentaire' ,'statut']

class ReviewRecourSerializer(serializers.ModelSerializer):
    status_projet =[
     ('approuvé','Approuvé'),
     ('rejeté', 'Rejeté'),
    ]
    statut= serializers.ChoiceField(choices=status_projet)
    class Meta:
      model = Review
      fields = ['statut']
        
class ComitéProjectListSerializer (serializers.ModelSerializer):
  reviews = ReviewSerializer( read_only=True )
  co_encadreur = serializers.StringRelatedField()
  url = serializers.HyperlinkedIdentityField(
        view_name='Projet-detail2',
        read_only=True,
        lookup_field = 'pk'
      )
  class Meta :
    model = Projet
    fields = ['url','co_encadreur', 'encadreur', 'file', 'nom_société','domaine_projet', 'theme', 'porteur_projet' , 'membre1' , 'membre2' , 'membre3' , 'membre4' , 'membre5' , 'reviews']  
    

class PlanifierPeriodeSerializer(serializers.ModelSerializer):
  url = serializers.HyperlinkedIdentityField(
        view_name='planifier-periode',
        read_only=True,
        lookup_field = 'pk'
      )
  class Meta:
    model = Periode
    fields =['url','nom_periode', 'date_debut', 'date_fin']
    read_only_fields = ['nom_periode']
    
    

#################################################### ENSEIGNANT USER ###################################################################

class DepotProjetEnseignatSerializer (serializers.Serializer) :
  class Meta :
    model = Projet
    fields = ['encadreur', 'file' , 'domaine_projet' , 'theme'  ]
    read_only_fields = ['encadreur']
   

    
