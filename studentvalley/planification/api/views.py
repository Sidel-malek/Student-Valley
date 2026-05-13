from .serializers import *
from accounts.models import *
from rest_framework import generics , status 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny 
from django.db.models import Q
from rest_framework.exceptions import ValidationError , APIException
from gestion_projet.models import Projet
from django.utils import timezone
from accounts.utils import Util
from django.core.exceptions import ObjectDoesNotExist
from .permissions import *
from gestion_projet.api.serializers import ComitéProjectListSerializer

############################################## CHEF SERVICE DE STAGE ###################################################
class ListProjetSoutenance (generics.ListAPIView):
  serializer_class= ListProjetSoutenanceSerializer 
  permission_classes = [ AllowAny, ]
    
  def get_queryset(self):
        queryset = Projet.objects.exclude(autorisation_soutenance ='')
        return queryset
      
class DetailListProjetSoutenance (generics.RetrieveAPIView):
  serializer_class= ListProjetSoutenanceSerializer 
  permission_classes = [AllowAny, ]
    
  def get_queryset(self):
        queryset = Projet.objects.filter(autorisation_soutenance__isnull=False )
        return queryset
  
  
class PlanificationSoutenance (generics.CreateAPIView):
  serializer_class= SoutenanceSerializer 
 # permission_classes= [AllowAny , IsPeriodeSoutenance]
  
  def create(self, request, *args, **kwargs):
            
            pk = self.kwargs['pk']
            projet  = Projet.objects.get(pk =pk)
            encadreur = projet.encadreur
            co_encadreur= projet.co_encadreur  
            
            try :
              président_jury =  Enseignant.objects.get(email=request.data.get('président_jury_email'))
              examinataire_1 =  Enseignant.objects.get(email=request.data.get('examinataire_1_email'))
              examinataire_2 =  Enseignant.objects.get(email=request.data.get('examinataire_2_email'))
              examinataire_3 =  Enseignant.objects.get(email=request.data.get('examinataire_3_email'))
            except Enseignant.DoesNotExist:
              raise APIException("Président jury n'est pas un enseignant")
            
            
            date = request.data.get('date')
            heure = request.data.get('heur')
            lieu = request.data.get('lieu')
            salle = request.data.get('salle')
            nature = request.data.get('nature')
            mode = request.data.get('mode')
            
            ''' Soutenance.objects.create(projet = projet , président_jury = président_jury ,
                            examinataire_1=examinataire_1 , examinataire_2=examinataire_2,
                            examinataire_3=examinataire_3, co_encadreur_jury = co_encadreur ,
                            encadreur_jury = encadreur , date=date , heur =heure ,lieu=lieu, salle=salle , nature=nature, mode=mode )'''
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(projet = projet , président_jury = président_jury ,
                            examinataire_1=examinataire_1 , examinataire_2=examinataire_2,
                            examinataire_3=examinataire_3, co_encadreur_jury = co_encadreur ,
                            encadreur_jury = encadreur )
            
            
            
            ##############################################################
            emails_invité=[
              serializer.instance.invité_1_email 
             
            ]
            subject_2 = 'Invitation Soutenance'
            link = 'http://127.0.0.1:8000/api/register/invité/'
            body_2= f"cher distinataire \n Vous avez choisi d'etre invité au soutenance de projet '{projet.theme}' \n  Qui etait est planifiée pour le {date} à {heure}.\n"\
              f"Lieu : {lieu}\n"\
              f"Salle : {salle}\n"\
              f"Mode : {mode}\n"\
              f"Nature : {nature}\n\n"\
              f"Enregister vous dans notre plateform pour plus d'information sur le projet via le lien {link} "\
              f"Cordialement,\nStudent Valley"
            data_2 = {
                     'subject':subject_2,
                     'body':body_2,
                     'to_email': emails_invité
                      }
    
            Util.send_email(data_2)
            ############################################################################# 
            emails_jury=[
               serializer.instance.président_jury.email ,
               serializer.instance.examinataire_1.email ,
               serializer.instance.examinataire_2.email ,
               serializer.instance.examinataire_3.email ,
               
              
            ]
            
            body_3 = f"Cher destinataire,\n\n"\
                 f"Vous avez choisi d'être jury pour la soutenance du projet '{projet.theme}', qui est prévue pour le {date} à {heure}.\n"\
                 f"Lieu : {lieu}\n"\
                 f"Salle : {salle}\n"\
                 f"Mode : {mode}\n"\
                 f"Nature : {nature}\n\n"\
                 f"Président du jury : {président_jury.first_name} {président_jury.last_name}\n"\
                 f"Premier examinateur du jury : {examinataire_1.first_name} {examinataire_1.last_name}\n"\
                 f"Deuxième examinateur du jury : {examinataire_2.first_name} {examinataire_2.last_name}\n"\
                 f"Troisième examinateur du jury : {examinataire_3.first_name} {examinataire_3.last_name}\n\n"\
                 f"Cordialement,\nStudent Valley"
            
            data_3 = {
                     'subject':subject_2,
                     'body':body_3,
                     'to_email': emails_jury
                      }
      
        
            Util.send_email(data_3)
            
            
            #######################################
            recipient_list =[]
            for  index in range(5) :
                if getattr(projet,f"membre{index+1}" ):
                   recipient_list.append(getattr(projet, f"membre{index+1}"))
                else :
                    index = index - 1
                    continue
             
            recipient_list.append(encadreur.email )
            recipient_list.append(co_encadreur.email )

            
            subject = 'Soutenance'
            body = f"Cher destinataire,\n\n"\
              f"Nous vous informons que la soutenance est planifiée pour le {date} à {heure}.\n"\
              f"Lieu : {lieu}\n"\
              f"Salle : {salle}\n"\
              f"Mode : {mode}\n"\
              f"Nature : {nature}\n\n"\
              f"Cordialement,\nStudent Valley"
            data = {
                     'subject':subject,
                     'body':body,
                     'to_email': recipient_list
                      }
      
            Util.send_email(data)
            
            
            
            
            return Response(status=status.HTTP_201_CREATED)
            


class UpdateSoutenance (generics.RetrieveUpdateDestroyAPIView):
  serializer_class = SoutenanceSerializer
  
  def get_object(self):
        pk = self.kwargs['pk']
        projet = Projet.objects.get(pk=pk)
        try:
            soutenance = Soutenance.objects.get(projet=projet)
            return soutenance
        except Soutenance.DoesNotExist:
            raise APIException({"detail": "Ce projet n'a pas de soutenance. Vous pouvez en créer une."})       
            
  
##################################################### ENSEIGNANT_USER ############################################################

class ListSoutnance(generics.ListAPIView):
  serializer_class = ListSoutenanceSerializer
  #permission_classes= [IsAuthenticated]

  def get_queryset(self):
        
        user = self.request.user
        enseignant = Enseignant.objects.get(email="prof1@gmail.com")#user.email
        projets = Projet.objects.filter(
            Q(encadreur=enseignant , statut='approuvé') |
            Q(co_encadreur=enseignant , statut='approuvé')
        )
        soutnances =[]
        for projet in projets:
            try:
              soutnance = Soutenance.objects.get(projet=projet)
            except Soutenance.DoesNotExist:
              continue
            soutnances.append(soutnance)
            
            
        
        return soutnances
      
class DetailListSoutnance(generics.RetrieveAPIView):
  serializer_class = ListSoutenanceSerializer
  queryset = Soutenance.objects.all()