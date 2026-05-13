from rest_framework import serializers
from accounts.models import Etudiant , Enseignant , MyUser
from gestion_projet.models import *
from planification.models import *



class ListProjetSoutenanceSerializer (serializers.ModelSerializer) :
     url_projet = serializers.HyperlinkedIdentityField(
        view_name='listprojet-detail',
        read_only=True,
        lookup_field = 'pk'
      )
     url_soutenance = serializers.HyperlinkedIdentityField(
        view_name='planification-soutenance',
        read_only=True,
        lookup_field = 'pk'
      )

     class Meta :
          model = Projet
          fields = [ 'url_projet', 'autorisation_soutenance','url_soutenance' ,'co_encadreur', 'encadreur', 'porteur_projet', 'nom_société' ,'domaine_projet' , 'theme'  , 'membre1', 'membre2' , 'membre3', 'membre4', 'membre5', ]
           
           
     
class SoutenanceSerializer(serializers.ModelSerializer):
    président_jury_email = serializers.EmailField()
    examinataire_1_email = serializers.EmailField()
    examinataire_2_email = serializers.EmailField()
    examinataire_3_email= serializers.EmailField()
    invité_1_email= serializers.EmailField()
    
    
    class Meta:
        model = Soutenance
        fields = ['date', 'heur', 'lieu', 'salle', 'mode', 'nature', 'président_jury_email', 'examinataire_1_email','examinataire_2_email','examinataire_3_email', 'invité_1_email'  ]
        read_only_fields = ['projet' , 'président_jury_email' ,'examinataire_1_email' , 'examinataire_2_email' , 'examinataire_3_email' ]
       
    def create(self, validated_data):
               validated_data.pop('président_jury_email', None)
               validated_data.pop( 'examinataire_1_email', None)
               validated_data.pop( 'examinataire_2_email', None)
               validated_data.pop( 'examinataire_3_email', None)
               return super().create(validated_data)

               

    def update(self, instance, validated_data):
        
                 validated_data.pop('président_jury_email', None)
                 validated_data.pop( 'examinataire_1_email', None)
                 validated_data.pop( 'examinataire_2_email', None)
                 validated_data.pop( 'examinataire_3_email', None)
                 
                 return super().update(instance, validated_data)
        
                

    def validate_date(self, date):
        date_fin = Periode.objects.get(nom_periode="Peroide de Soutenance").date_fin
        if date > date_fin:
            raise serializers.ValidationError("La date dépasse la date de fin de soutenance.")
        return date
    
    

class ListSoutenanceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='listsoutenance-detail',
        read_only=True,
        lookup_field='pk'
    )

    class Meta:
        model = Soutenance
        fields = ['url', 'date', 'heur', 'lieu', 'salle', 'mode', 'nature', 'jury']
        read_only_fields = ['projet']