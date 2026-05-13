from rest_framework import permissions
from accounts.models import *
from gestion_projet.models import *
import datetime
from rest_framework.exceptions import APIException



class IsPorteurProjetOrMember(permissions.BasePermission):
  
   def has_object_permission(self, request, view, obj):
        user = request.user
        etudiant = Etudiant.objects.get(email=user.email)
        
        if view.action == 'retrieve':
            # Allow view (retrieve) permission to users in the "porteur_projet" group and project members
            return True
          
        if view.action in ['update', 'partial_update', 'destroy']:
            # Allow update and delete permissions only to users in the "porteur_projet" group
            return etudiant.role.filter(name='PorteurProjet').exists()
          
        return False
    
    
class IsMembreComite(permissions.BasePermission):
    def has_permission(self, request, view):
        member = MyUser.objects.get(email= request.user.email)
        if member.role.filter(name='MembreComité').exists() or member.role.filter(name='ResponsableComité').exists(): 
           return True
        else : return False 

class IsResponsableComite(permissions.BasePermission):
    def has_permission(self, request, view):
        member = MyUser.objects.filter(email= request.user.email).exists()
        if member.role.filter(name='ResponsableComité').exists(): 
           return True
        else : return False 
    
class IsPeriodeValidation(permissions.BasePermission):
    
    def has_permission(self, request, view):
        periode_validation = Periode.objects.get(nom_periode="validation_projet")
        periode = datetime.date.today() >= periode_validation.date_debut 
        
        if periode:
            return True
        else:
            raise APIException(detail="La période de validation des projets n'est pas active.") 
        
class IsPeriodeValidationReview (permissions.BasePermission):
    
    def has_permission(self, request, view):
        periode_validation = Periode.objects.get(nom_periode="validation_projet")
        periode = datetime.date.today() >= periode_validation.date_debut and datetime.date.today() < periode_validation.date_fin
        
        if periode:
            return True
        elif datetime.date.today() < periode_validation.date_debut:
            raise APIException(detail="La période de depot des projets n'est pas active.") 
        
        else:
            raise APIException(detail="La période de depot des projets n'est pas active.") 
        
        
class IsPeriodeDepot(permissions.BasePermission):
    
    def has_permission(self, request, view):
        periode_depot = Periode.objects.get(nom_periode="depot_projet")
        periode = datetime.date.today() >= periode_depot.date_debut and datetime.date.today() < periode_depot.date_fin
        
        if periode:
            return True
        elif datetime.date.today() < periode_depot.date_debut:
            raise APIException(detail="La période de depot des projets n'est pas active.") 
        
        else:
            raise APIException(detail="La période de depot des projets n'est pas active.") 

class IsPeriodeRrcoursAndEnattente (permissions.BasePermission):
    
    def has_permission(self, request, view):
        periode_depot = Periode.objects.get(nom_periode="recours_periode")
        periode = datetime.date.today() >= periode_depot.date_debut and datetime.date.today() < periode_depot.date_fin
        
        if periode:
            user = Etudiant.objects.get(email="admin@esi-sba.dz")
            statut = Projet.objects.get(porteur_projet=user).statut
            if statut== 'en_attente':
               return True
            else: 
                return False
            
        elif datetime.date.today() < periode_depot.date_debut:
            raise APIException(detail="La période de recours des projets n'est pas active.") 
        
        
        else:
            raise APIException(detail="La période de recours des projets n'est pas active.") 

class IsPeriodeValidationRecoursReview (permissions.BasePermission):
    
    def has_permission(self, request, view):
        periode_validation_recours = Periode.objects.get(nom_periode="validation_recours_periode")
        periode = datetime.date.today() >= periode_validation_recours.date_debut and datetime.date.today() < periode_validation_recours.date_fin
        
        if periode:
            return True
        elif datetime.date.today() < periode_validation_recours.date_debut:
            raise APIException(detail="La période de depot des projets n'est pas active.") 
        
        else:
            raise APIException(detail="La période de depot des projets n'est pas active.") 
        
class IsPeriodeValidationRecours (permissions.BasePermission):
    
    def has_permission(self, request, view):
        periode_validation_recours = Periode.objects.get(nom_periode="validation_recours_periode")
        periode = datetime.date.today() >= periode_validation_recours.date_debut 
        
        if periode:
            return True
        else:
            raise APIException(detail="La période de validation des projets n'est pas active.") 
        
class IsNotMember(permissions.BasePermission):
    def has_permission(self, request, view):
        
        try:
            member = Etudiant.objects.get(email='admin@esi.dz')
        except Etudiant.DoesNotExist:
            return False
        
        if member.role.filter(name='MembreProjet').exists():
            raise APIException(detail="Vous ne pouvez pas déposer un projet.")
        else:
            return True
        



class IsPeriodeDepotOuRecours(permissions.BasePermission):
        def has_permission(self, request, view):
            periode_depot = Periode.objects.get(nom_periode="depot_projet")
            periode_recours = Periode.objects.get(nom_periode="recours_periode")

            periode_d = datetime.date.today() >= periode_depot.date_debut and datetime.date.today() < periode_depot.date_fin
            periode_r=  datetime.date.today() >= periode_recours.date_debut and datetime.date.today() < periode_recours.date_fin
            
            user = Etudiant.objects.get(email="admin@esi-sba.dz")
            statut = Projet.objects.get(porteur_projet=user).statut
            if periode_d or (periode_r and  statut== 'en_attente') :
                return True
            elif not periode_r:
                return 