from rest_framework import permissions
from accounts.models import *
from gestion_projet.models import *
import datetime
from rest_framework.exceptions import APIException

class IsPeriodeSoutenance(permissions.BasePermission):
    
    def has_permission(self, request, view):
        periode_depot = Periode.objects.get(nom_periode="Peroide de Soutenance")
        periode = datetime.date.today() < periode_depot.date_fin
        
        if periode:
            return True

        else:
            raise APIException(detail="La période de Soutenance est terminé.") 