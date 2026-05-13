from django.urls import path
from .views import *


urlpatterns = [
    # service de stages
    path('api/listprojet/', ListProjetSoutenance.as_view() , name='listprojet'),
    path('api/listprojet/<int:pk>', DetailListProjetSoutenance.as_view() , name='listprojet-detail'), 
    path('api/listprojet/<int:pk>/create-soutenance', PlanificationSoutenance.as_view() , name='planification-soutenance'),
    path('api/listprojet/<int:pk>/retrieve-soutenance', UpdateSoutenance.as_view() , name='update-soutenance'),
    # enseignant
    path('api/listsoutenance/', ListSoutnance.as_view() , name='list-soutenance'),
    path('api/listsoutenance/<int:pk>/', DetailListSoutnance.as_view() , name='listsoutenance-detail'),

]
