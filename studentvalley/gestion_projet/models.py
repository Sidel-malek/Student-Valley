from django.db import models
from accounts.models import Enseignant , Etudiant
from django.conf import settings
from django.core.validators import FileExtensionValidator

def get_emails_enseignants():
    enseignants = Enseignant.objects.all()
    emails = [enseignant.email for enseignant in enseignants]
    return emails
  
class Projet (models.Model):
  membre1_email= models.EmailField(max_length=255 , blank=True, null=True)
  membre2_email= models.EmailField(max_length=255, blank=True, null=True)
  membre3_email= models.EmailField(max_length=255, blank=True, null=True)
  membre4_email= models.EmailField(max_length=255, blank=True, null=True)
  membre5_email= models.EmailField(max_length=255, blank=True, null=True)
  
  DOMAINE = [
    ("Informatique", "Informatique"),
    ("Social", "Social"),
    ("Médcine", "Médcine"),
    ("Agriculture", "Agriculture"),
    ("Médicale", "Médicale"),
  ]
  TYPE_DEMANDE_CHOICES = [
        ('un diplôme-une startup', 'un diplôme-une startup'),
        ('un diplôme-un brevet', 'un diplôme-une brevet'),
        
        # Ajoutez d'autres types de demandes si nécessaire
  ]
  STATUT_CHOICES = [
        ('approuvé', 'Approuvé'),
        ('en_attente', 'En attente'),
        ('rejeté', 'Rejeté'),
    ]
  autorisation_soutenance = models.FileField(upload_to='fiches_techniques/', blank=True, null=True , default=None)   
  statut = models.CharField(max_length=20, choices=STATUT_CHOICES, blank= True, null=True)
  theme = models.CharField(max_length=500)
  domaine_projet = models.CharField(choices=DOMAINE , max_length=50)
  nom_société = models.CharField(max_length=20 , unique=True)
  file = models.FileField(upload_to='fiches_techniques/', blank=True, null=True)   

  date_depot = models.DateField(auto_now_add=True)
  encadreur = models.ForeignKey(Enseignant, on_delete=models.CASCADE, null=True, blank=True, related_name='projets_encadres',default= get_emails_enseignants)
  co_encadreur = models.ForeignKey(Enseignant, on_delete=models.CASCADE, null=True, blank=True, related_name='projets_co_encadres',default = get_emails_enseignants)
  porteur_projet = models.OneToOneField( Etudiant , on_delete=models.CASCADE , related_name='prteur_projet', blank=True , null=True)
  membre1 = models.OneToOneField(Etudiant,on_delete=models.CASCADE , null=True, blank=True ,related_name='membre1_projet')
  membre2 = models.OneToOneField(Etudiant, on_delete=models.CASCADE , null=True, blank=True ,related_name='membre2_projet')
  membre3 = models.OneToOneField(Etudiant, on_delete=models.CASCADE, null=True, blank=True, related_name='membre3_projet')
  membre4 = models.OneToOneField(Etudiant,  on_delete=models.CASCADE, null=True, blank=True , related_name='membre4_projet')
  membre5 = models.OneToOneField(Etudiant, on_delete=models.CASCADE, null=True, blank=True , related_name='membre5_projet')
  
  def __str__(self):
    return self.theme

  
class Periode (models.Model):
  date_debut = models.DateField()
  date_fin = models.DateField()
  nom_periode = models.CharField(max_length=30)
  
  def __str__(self):
    return self.nom_periode
  
class Modification (models.Model):
  date_modification = models.DateTimeField()
  projet= models.ForeignKey(Projet , on_delete=models.CASCADE )
  def __str__(self):
    return self.projet.theme
  
'''class Recours (models.Model):
  descripption = models.CharField(max_length=200)
  projet = models.OneToOneField(Projet, on_delete=models.CASCADE)
  def __str__(self):
    return self.projet.theme'''
  

class Review (models.Model):
  
    STATUT_CHOICES = [
        ('approuvé', 'Approuvé'),
        ('en_attente', 'En attente'),
        ('rejeté', 'Rejeté'),
    ]
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, blank= True, null=True)
    commentaire = models.CharField(max_length=200 , blank= True, null=True)
    crée = models.DateTimeField(auto_now_add=True)
    projet = models.OneToOneField( Projet , on_delete=models.CASCADE , related_name="reviews")
    
    def __str__(self):
        return  self.projet.theme
  
  
  
  


    
    
   

   
   
    
       