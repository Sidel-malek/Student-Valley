from django.db import models
from gestion_projet.models import Projet
from accounts.models import MyUser , Enseignant

class Soutenance (models.Model):
  projet= models.OneToOneField(Projet ,on_delete=models.CASCADE )
  date = models.DateField()
  heur = models.TimeField()
  lieu = models.CharField(max_length=20)
  salle= models.CharField(max_length=20)
  CHOIX_MODE =[
    ('présentiel', 'présentiel'),
    ('distance', 'distance')
  ]
  mode = models.CharField(max_length=20, choices=CHOIX_MODE)
  
  CHOIX_NATURE =[
    ('ouverte', 'ouverte'),
    ('à huis clos', 'à huis clos')
  ]
  nature = models.CharField(max_length=20, choices=CHOIX_NATURE)
  président_jury = models.ForeignKey(Enseignant , on_delete= models.CASCADE , related_name='président_jury' )
  encadreur_jury = models.ForeignKey(Enseignant , on_delete= models.CASCADE , related_name='encadreur_jury')
  co_encadreur_jury =  models.ForeignKey(Enseignant , on_delete= models.CASCADE , related_name='co_encadreur_jury')
  examinataire_1 = models.ForeignKey(Enseignant , on_delete= models.CASCADE , related_name='exa1_jury')
  examinataire_2 =models.ForeignKey(Enseignant , on_delete= models.CASCADE , related_name='exa2_jury')
  examinataire_3 =models.ForeignKey(Enseignant , on_delete= models.CASCADE , related_name='exa3_jury')
  invité_1 = models.ForeignKey(MyUser , blank=True , null=True , on_delete= models.CASCADE , related_name='invité_1' )
  invité_1_email = models.EmailField(MyUser , blank=True , null=True  )
 
  
  
  
  

