from .serializers import *
from accounts.models import *
from rest_framework import generics , status 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from django.db.models import Q
from rest_framework.exceptions import ValidationError , APIException
from gestion_projet.models import Projet
from .permissions import *
from django.utils import timezone
from accounts.utils import Util
from django.core.exceptions import ObjectDoesNotExist



#################################################### ETUDIANT_USER ###################################################################

'''******************************************  DEPOT DE PROJET ET CREATION DE GTOUPE  **********************************************************'''

class DépotProjetView(generics.CreateAPIView ): 
   # permission_classes = [ IsPeriodeDepot , IsNotMember ]
   # permission_classes=[IsAuthenticated]
    serializer_class = ProjetDepotSerializer
    queryset= Projet.objects.none()
    
    def get (self, request):
        return Response({"Note":"be sure that members are registed in this platform or send him invitaion first"})
    
    def create(self, request, *args, **kwargs):
            group1 = Group.objects.get(name='PorteurProjet')
            group2 = Group.objects.get(name='Encadreur')
            group3 = Group.objects.get(name='Co-encadreur')
            group4 = Group.objects.get(name='MembreProjet')
            
            porteur_projet = Etudiant.objects.get(email='ma@esi-sba.dz')   #request.email
            porteur_projet.role.add(group1)
            
            projet_theme = request.data.get('theme')
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
           
            
            encadreur = request.data.get('encadreur_email')
            if encadreur:
                encadreur_obj = Enseignant.objects.get(email=encadreur)
                encadreur_obj.role.add(group2)

            co_encadreur = request.data.get('co_encadreur_email')
            if co_encadreur:
                co_encadreur_obj = Enseignant.objects.get(email=co_encadreur)
                co_encadreur_obj.role.add(group3) 
            
            members_emails =[
                'membre1_email',
                'membre2_email',
                'membre3_email',
                'membre4_email',
                'membre5_email'
            ]
            members = []
            
            for index, member in enumerate(members_emails, start=1):
              if serializer.validated_data.get(member) != '':
                members.append(serializer.validated_data.get(member))
            
             # Check for duplicates
            if len(set(members)) != len(members):
                    return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'Duplicate members are not allowed.'})
                    
            print(members)       
           
            co_encadreur_obj = Enseignant.objects.get(email=co_encadreur)
            encadreur_obj = Enseignant.objects.get(email=encadreur)
            serializer.save(porteur_projet=porteur_projet , encadreur=encadreur_obj , co_encadreur= co_encadreur_obj)
            
            projet = serializer.instance
            not_exist=[]
            
            for index, member in enumerate(members, start=1):
             if member:  
                
                try:
                    etudiant = Etudiant.objects.get(email=member)
                    setattr(projet, f"membre{index}", etudiant)
                    etudiant.role.add(group4)
                    etudiant.save()
                    subject = "Projet Student Valley"
                    link = 'http://127.0.0.1:8000/api/login/'
                    body = f"cher membre vous avez choisi de participer dans un projet de fin d'étude qui a pour thème <<{projet_theme}>>.\n\nPour plus de détails, veuillez vérifier votre compte sur {link}.\n\nCordialement.\n\nStudent Valley"
                    data = {
                        'subject': subject,
                        'body': body,
                        'to_email': (member,)
                    }
                    Util.send_email(data)
                    
                except Etudiant.DoesNotExist:
                    not_exist.append(member)
                    subject = "Projet Student Vlley"
                    link = 'http://127.0.0.1:8000/api/register/'
                    body = f"cher etudiant vous avez choisé pour participer dans un projet de fin d'etude qui a pour theme <<{projet_theme}>> , \n pour plus de detail crée votre compte dans notre platform via ce link  {link}.\n\n Cordialement. \n\n Student Valley  "
                    data = {
                     'subject':subject,
                     'body':body,
                     'to_email':( member ,)
                      }
                    
                    Util.send_email(data)
                    continue
            
                
                
                

                projet.save()
                
            if not_exist : 
               return Response(data={'We have invite eudiant with this email to participate with you in this project ': not_exist}) 
            else :
                 return Response(data={'message': 'Votre projet a été créé avec succès.'}, status=status.HTTP_201_CREATED)


'''******************************************  LIST DE PROJET  *****************************************************'''
      
class ListProjet (generics.ListAPIView):
    
  #permission_classes= [IsAuthenticated]
  serializer_class = ListProjetSerializer
  queryset = Projet.objects.all()



class PrendProjet (generics.RetrieveUpdateAPIView):
    serializer_class = ProjetDepotSerializer
    def perform_update(self, serializer):
        
            group1 = Group.objects.get(name='PorteurProjet')
            group2 = Group.objects.get(name='Encadreur')
            group3 = Group.objects.get(name='Co-encadreur')
            group4 = Group.objects.get(name='MembreProjet')
            
            porteur_projet = Etudiant.objects.get(email='admin@esi-sba.dz')   
            porteur_projet.role.add(group1)
            
            co_encadreur = serializer.validated_data.get('co-encadreur')
            if co_encadreur:
                co_encadreur_obj = Enseignant.objects.get(id=co_encadreur)
                co_encadreur_obj.role.add(group3) 
        
            
            members = []
            for index, member in enumerate(members, start=1):
              if serializer.validated_data.get('membre1_email') != '':
                members.append(serializer.validated_data.get('membremembre1_email'))
                
            serializer.validated_data.get('membre1_email'),
            serializer.validated_data.get('membre2_email'),
            serializer.validated_data.get('membre3_email'),
            serializer.validated_data.get('membre4_email'),
            serializer.validated_data.get('membre5_email')
            
             # Check for duplicates
             
            if len(set(members)) != len(members) :
                    return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'Duplicate members are not allowed.'})
                    
                   
            
            projet_theme = serializer.validated_data.get('theme')
            
            super().perform_update(serializer) 
            
            
            projet = serializer.instance
            not_exist=[]
            
            for index, member in enumerate(members, start=1):
             if member:  
                
                try:
                    etudiant = Etudiant.objects.get(email=member)
                    setattr(projet, f"membre{index}", etudiant)
                    etudiant.role.add(group4)
                    etudiant.save()
                    subject = "Projet Student Valley"
                    link = 'http://127.0.0.1:8000/api/login/'
                    body = f"cher membre vous avez choisi de participer dans un projet de fin d'étude qui a pour thème <<{projet_theme}>>.\n\nPour plus de détails, veuillez vérifier votre compte sur {link}.\n\nCordialement.\n\nStudent Valley"
                    data = {
                        'subject': subject,
                        'body': body,
                        'to_email': (member,)
                    }
                    Util.send_email(data)
                    
                except Etudiant.DoesNotExist:
                    not_exist.append(member)
                    subject = "Projet Student Vlley"
                    link = 'http://127.0.0.1:8000/api/register/'
                    body = f"cher etudiant vous avez choisé pour participer dans un projet de fin d'etude qui a pour theme <<{projet_theme}>> , \n pour plus de detail crée votre compte dans notre platform via ce link  {link}.\n\n Cordialement. \n\n Student Valley  "
                    data = {
                     'subject':subject,
                     'body':body,
                     'to_email':( member ,)
                      }
                    
                    Util.send_email(data)
                    continue
                
                
                
            if not_exist : 
               return Response(data={'We have invite eudiant with this email to participate with you in this project ': not_exist}) 
            else :
                 return Response(data={'message': 'Votre projet a été créé avec succès.'}, status=status.HTTP_201_CREATED)




   
'''******************************************  DEATAIL D'UN PROJET DE LIST  *****************************************************'''

class DetailProjetList (generics.RetrieveAPIView):
  #permission_classes= [IsAuthenticated]
  serializer_class= ListProjetSerializer
  queryset = Projet.objects.all()

'''******************************************  MODIFIER LEUR PROJET AVANT LE DELAI  *****************************************************'''

class ProjectDetailView(generics.RetrieveAPIView):
   # permission_classes= [IsAuthenticated]
    serializer_class = OwnerProjectDetailSerializer
    def get_object(self):
        try:
             user = Etudiant.objects.get(email='admin@esi-sba.dz')  
        except Etudiant.DoesNotExist:        
            raise ValidationError("You are not Student.", code='invalid')
        try:
           project = Projet.objects.get(porteur_projet=user)
        except Projet.DoesNotExist:       
                raise ValidationError("Project not found or you are not leader of this project ." , code='invalide')
        return project 


class ProjectUpdate (generics.RetrieveUpdateAPIView) :
   # permission_classes = [   IsPeriodeRrcoursAndEnattente ]
    serializer_class = ProjetDepotSerializer
    #queryset = Projet.objects.none()
    
    def get_object(self):
        try:
             user = Etudiant.objects.get(email=self.request.user.email) # self.request.user.email
        except Etudiant.DoesNotExist:        
            raise ValidationError("You are not Student.", code='invalid')
        try:
           project = Projet.objects.get(porteur_projet=user)
        except Projet.DoesNotExist:       
                raise ValidationError("Project not found or you are not leader of this project ." , code='invalide')
            
        return project 
    
    
    def perform_update(self, serializer):
            Modification.objects.create(projet=self.get_object() , 
                                        date_modification= timezone.now().strftime('%Y-%m-%d/%H:%M'))  
            
            updated_emails = []
            for membre_email in ['membre1_email', 'membre2_email', 'membre3_email', 'membre4_email', 'membre5_email']:
                updated_email = serializer.validated_data.get(membre_email)
                if updated_email and updated_email != getattr(self.get_object(), membre_email):
                     updated_emails.append(updated_email)
             
            super().perform_update(serializer)
            
            subject = 'Invitation StudentValley'             # Send EMail
            body = f"cher destinataire vous avez choisé pour participer avec le groupe '{self.get_object().nom_société}' dans le projet de fin etude sous le nom '{self.get_object().theme} "
            data = {
                     'subject':subject,
                     'body':body,
                     'to_email': updated_emails
                      }
      
            Util.send_email(data)
        
        
        
class ProjectDestroy(generics.DestroyAPIView) :
    #permission_classes = [ IsPeriodeDepot   ,IsAuthenticated ]
    serializer_class = ProjetDepotSerializer
    queryset = Projet.objects.none()
    
    def destroy(self, request, *args, **kwargs):
            pk = self.kwargs['pk']  
            project = Projet.objects.get(pk=pk)
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
'''******************************************  ETAT DE PROJET  *****************************************************'''

class EtatProjet(generics.GenericAPIView):
    serializer_class = EtatProjetSerializer
    
    def get(self, request, *args, **kwargs):
        
        user = Etudiant.objects.get(email=request.user.email)#request.user
        
        projet = Projet.objects.filter(
            Q(porteur_projet=user) | Q(membre1=user) | Q(membre2=user) | Q(membre3=user) | Q(membre4=user) | Q(membre5=user)
          ).last()
        
        periode = Periode.objects.get(nom_periode="depot_projet")
        date_debut = periode.date_debut
        print(date_debut)
        date_fin = periode.date_fin
        print(date_fin)
        date_depot = projet.date_depot if projet else None
        
        latest_modification = Modification.objects.filter(projet=projet).last()
        derniere_modification = latest_modification.date_modification if latest_modification else None
        
        try:
            review = Review.objects.get(projet=projet)
            commentaire = review.commentaire
            statut_projet = review.statut
        except ObjectDoesNotExist:
            commentaire = None
            statut_projet = None
        
        data = {
            'date_debut': date_debut,
            'date_fin': date_fin,
            'derniere_modification': derniere_modification,
            'date_depot': date_depot,
            'commentaire': commentaire,
            'statut_projet': statut_projet,
        }
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.validated_data
        
        return Response(serialized_data, status=status.HTTP_200_OK)
        
    
'''****************************************************  RECOURS DE PROJET **********************************************************'''

'''class RecourProjet(generics.CreateAPIView):
    serializer_class = ListRecourProjetSerializer
    permission_classes = [IsPeriodeRrcours ]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            etudiant = Etudiant.objects.get(email=request.user.email)  
        except Etudiant.DoesNotExist:
            raise APIException("You are not allowed to perform this action")
        
        try:
            projet = Projet.objects.get(porteur_projet=etudiant , statut='en_attente')
            print(projet)
            serializer.validated_data['projet'] = projet
            serializer.save(projet=projet)
            return Response (serializer.data , status=status.HTTP_200_OK)
        
        except Projet.DoesNotExist:
            raise APIException("You are not allowed to perform this action")'''



#################################################### COMITE_SCIENTIFIQUE_USER ###################################################################

      
class ListeProjetsComité(generics.ListAPIView):
   serializer_class = ComitéProjectListSerializer
  # permission_classes = [IsAuthenticated, IsMembreComite, IsPeriodeValidation ]
   queryset = Projet.objects.all()
   


class DetailListeProjetsComité (generics.RetrieveAPIView):
    permission_classes = [ IsPeriodeValidation ]
   # permission_classes= [IsAuthenticated ,IsMembreComite , IsPeriodeValidation]
    serializer_class= ComitéProjectListSerializer
    queryset = Projet.objects.all()
          
            

class ReviewListAV (generics.ListAPIView):
   #permission_classes= [IsAuthenticated , IsMembreComite , IsPeriodeValidation]
   serializer_class= ReviewSerializer

   
   def get_queryset(self):
          pk = self.kwargs['pk']
          return Review.objects.filter(projet =pk)
                

class ApprobationReviewCreateAV (generics.CreateAPIView):
   # permission_classes= [IsAuthenticated ,IsResponsableComite ,IsPeriodeValidationReview ]
    serializer_class= ReviewSerializer
   
    def perform_create(self, serializer):
       
            pk = self.kwargs['pk']
            projet = Projet.objects.get(pk =pk)
            
            serializer.save(projet = projet)
            
            recipient_list =[]
            
            recipient_list.append(getattr(projet,'porteur_projet' ).email)
            recipient_list.append(getattr(projet,'encadreur' ).email)
            recipient_list.append(getattr(projet,'co_encadreur' ).email)
            for  index in range(1,5) :
                if getattr(projet,f"membre{index}" ):
                   recipient_list.append(getattr(projet, f"membre{index}"))
                else :
                    index = index - 1
                    continue
            print(recipient_list)    
            link = 'http://127.0.0.1:8000/api/register/'
           
            subject = 'Approbation De Votre Projet'
            
            
            if serializer.data['statut']== 'approuvé' :
                projet.statut = 'approuvé'
                projet.save()
                # Send EMail
                body = f"Dear members,\n\nCongratulations!!! Your project '{projet.theme}' has been approved. We are pleased to inform you that your hard work and dedication have paid off. We appreciate your contribution to our organization.\n access the platform using the provided link and check the statut of your project '{link}'.\n\nBest regards,\nYour Organization "
                data = {
                     'subject':subject,
                     'body':body,
                     'to_email': recipient_list
                      }
      
                Util.send_email(data)
               
               
            if serializer.data['statut']== 'en_attente' :
                projet.statut = 'en_attente'
                projet.save()
                # Send EMail
                body = f"Cher(e) etudiant(e),\n\nNous vous informons que votre projet intitulé '{projet.theme}' est actuellement en réserve. Le comité scientifique a fourni des commentaires et des recommandations pour améliorer votre projet.\n\nVous pouvez vous connecter à la plateforme et accéder à la section 'Statut du projet' pour consulter les commentaires détaillés du comité scientifique{link}. Vous êtes encouragé(e) à prendre en compte ces commentaires et à modifier votre projet en conséquence.\n\nCordialement,\nVotre Organisation"
                data = {
                     'subject':subject,
                     'body':body,
                     'to_email': recipient_list
                      }
      
                Util.send_email(data)
               
               
            if serializer.data['statut']== 'rejeté' :
                projet.statut = 'rejeté'
                projet.save()
                # Send EMail
                body = f"Cher(e) porteur(e) de projet,\n\nNous regrettons de vous informer que votre projet intitulé '{projet.theme}' a été rejeté. Malheureusement, il ne répond pas aux critères requis pour l'approbation.\n\nVous pouvez vous connecter à la plateforme pour obtenir plus de détails sur le statut de votre projet et la raison du rejet '{link}'.\n\nCordialement,\nStudent Valley"
                data = {
                     'subject':subject,
                     'body':body,
                     'to_email': recipient_list
                      }
      
                Util.send_email(data)
                
                for user_email in recipient_list :
                    user = MyUser.objects.get(email=user_email)    
                    user.is_active=False
                    user.save()
                    
                    
                    
class ListRecourProjet ( generics.ListAPIView) :
   # permission_classes= [IsAuthenticated]
    serializer_class = ComitéProjectListSerializer
    def get_queryset(self):
        
        periode_recours = Periode.objects.get(nom_periode="recours_periode")
        date_modification = Modification.objects.all()
        projet =[]
        for date in date_modification:
            if date.date_modification.date() >= periode_recours.date_debut and date.date_modification.date() <= periode_recours.date_fin:
               projet.append(date.projet)  
        
        
        
        queryset = projet
        return queryset
  

                   
class ReviewRecours (generics.CreateAPIView) :
    serializer_class= ReviewRecourSerializer
   # permission_classes =[IsPeriodeValidationRecoursReview , IsMembreComite, IsAuthenticated]
    
    def perform_create(self, serializer):
       
            pk = self.kwargs['pk']
            projet = Projet.objects.get(pk =pk)
            serializer.save(projet = projet)
            recipient_list =[]
            for  index in range(5) :
                
                if getattr(projet,f"membre{index+1}" ):
                   recipient_list.append(getattr(projet, f"membre{index+1}"))
                else :
                    index = index - 1
                    continue
            link = 'http://127.0.0.1:8000/api/register/'
           
            link = 'http://127.0.0.1:8000/api/register/'
            subject = 'Resultat De Recours'
            
            
            
            if serializer.data['statut']== 'approuvé' :
                projet.statut = 'en_attente'
                projet.save()
               # Send EMail
                body = f"Dear members ,\n\nCongratulations!!! Your project '{projet.theme}' has been approved. We are pleased to inform you that your hard work and dedication have paid off. We appreciate your contribution to our organization.\n access the platform using the provided link and check the statut of your project '{link}'.\n\nBest regards,\nYour Organization "
                
                data = {
                     'subject':subject,
                     'body':body,
                     'to_email': recipient_list
                      }
      
                Util.send_email(data)
               
               
            if serializer.data['statut']== 'rejeté' :
                projet.statut = 'rejeté'
                projet.save()
                for user_email in recipient_list :
                    user = MyUser.objects.get(email=user_email)    
                    user.is_active = False
                    user.save()
                # Send EMail
                body = f"Cher(e) porteur(e) de projet,\n\nNous regrettons de vous informer que votre projet intitulé '{projet.theme}' a été rejeté. Malheureusement, il ne répond pas aux critères requis pour l'approbation.\n\nVous pouvez vous connecter à la plateforme pour obtenir plus de détails sur le statut de votre projet et la raison du rejet '{link}'.\n\nCordialement,\nStudent Valley"
                data = {
                     'subject':subject,
                     'body':body,
                     'to_email': recipient_list
                      }
           
                Util.send_email(data)
                
            
            
            
class ListPeriode (generics.ListAPIView):
  #permission_classes= [IsAuthenticated , IsMembreComite]
  serializer_class = PlanifierPeriodeSerializer
  queryset = Periode.objects.all()
              
              
              
class PlanifierPeriode (generics.RetrieveUpdateAPIView):
    #permission_classes= [IsAuthenticated, IsMembreComite]
    serializer_class = PlanifierPeriodeSerializer
    queryset = Periode.objects.all()
    
    
    
    
#################################################### ENSEIGNANT_USER ###################################################################

class ListProjetEncadré (generics.ListAPIView) :
    permission_classes= [IsAuthenticated]
    serializer_class = ComitéProjectListSerializer
    
    def get_queryset(self):
        
        user = self.request.user
        enseignant = Enseignant.objects.get(email='admin@esi-sba.dz')
        queryset = Projet.objects.filter(
            Q(encadreur=enseignant , statut='approuvé') |
            Q(co_encadreur=enseignant , statut='approuvé')
        )
        return queryset

class DetailProjetEncadré (generics.RetrieveAPIView) :
    #permission_classes= [IsAuthenticated]
    serializer_class = ComitéProjectListSerializer
    def get_queryset(self):
        
        user = self.request.user
        enseignant = Enseignant.objects.get(email=user.email)
        
        queryset = Projet.objects.filter(
            Q(encadreur=enseignant , statut='approuvé') |
            Q(co_encadreur=enseignant , statut='approuvé')
        )
        return queryset

class DepotProjetEnseignat (generics.CreateAPIView):
    permission_classes=[]
    serializer_class =   DepotProjetEnseignatSerializer  
    
    def create(self, request, *args, **kwargs):
          
            group3 = Group.objects.get(name='Encadreur')
            
            encadreur = request.user
            if encadreur:
                encadreur_obj = Enseignant.objects.get(id=encadreur)
                encadreur_obj.role.add(group3)
        
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(encadreur=encadreur_obj)


    

####################################################################################################################################################

    
class HasProjet(generics.GenericAPIView):
    def get(self, request):

        user = request.user
        etudiant = Etudiant.objects.get(email=user.email)

        
        if Projet.objects.filter(
            Q(porteur_projet=etudiant) |
            Q(membre1=etudiant) |
            Q(membre2=etudiant) |
            Q(membre3=etudiant) |
            Q(membre4=etudiant) |
            Q(membre5=etudiant)
        ).exists() :
             data = {'has_project': True}
        else :
             data = {'has_project': False}
        return Response(data)













