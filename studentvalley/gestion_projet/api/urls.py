from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns =[

    path('api/etudiant/hasprojet/', HasProjet.as_view(), name='has_project'),
    ## etudiant
    path('api/etudiant/depot-projet/', DépotProjetView.as_view(), name='depot-projet'),
    path('api/etudiant/listprojet/', ListProjet.as_view(), name='Projet'), 
    path('api/etudiant/list-projet/<int:pk>/', DetailProjetList.as_view(), name='Projet-detail'),
    path('api/owner/projetdetail/', ProjectDetailView.as_view(), name='my-projet-detail'),
    path('api/owner/updateprojet/', ProjectUpdate.as_view(), name='info-projet-update'),
    path('api/owner/destroyprojet/', ProjectDestroy.as_view(), name='info-projet-update'),
    path('api/owner/etatprojet/', EtatProjet.as_view(), name='etat-projet'),
  
    
    ## comité_scientifique 
    path('api/comite/listprojet/', ListeProjetsComité.as_view(), name='liste_projets'),
    path('api/comite/listprojet/<int:pk>/', DetailListeProjetsComité.as_view(), name='Projet-detail2'),
    path('api/comite/listprojet/<int:pk>/review/', ReviewListAV.as_view(), name='Projet-review'),
    path('api/comite/listprojet/<int:pk>/review/create/', ApprobationReviewCreateAV.as_view(), name='Projet-review-create'),
    path('api/comite/listperiode/' , ListPeriode.as_view(), name='ListPeriode'),
    path('api/comite/listperiode/<int:pk>/', PlanifierPeriode.as_view(), name='planifier-periode'),
    path('api/comite/recours/listprojet/' , ListRecourProjet.as_view(), name='recours-list'),
    path('api/comite/recours/listprojet/<int:pk>/' , DetailListeProjetsComité.as_view(), name='recours-detail'),
    path('api/comite/recours/listprojet/<int:pk>/review/create' , ReviewRecours.as_view(), name='recours-review'),

    
    
    ## enseignant
    path('api/enseignant/listprojet/', ListProjetEncadré.as_view(), name='list-projt-encadré'),
    path('api/enseignant/listprojet/<int:pk>/', DetailProjetEncadré.as_view(), name='list-projt-encadré'),
    
    
 
 ]+static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)

    
