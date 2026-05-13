from django.db import models
from django.db import models
from django.contrib.auth.models import  Group , PermissionsMixin, AbstractBaseUser,BaseUserManager, AbstractUser , UserManager
from django.contrib import admin
from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField
#from django.utils.text import slugify
# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name,  **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, numero_telephone, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_admin',False)
        return self._create_user(email, password, first_name, last_name, numero_telephone, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name,  **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_admin',True)
        return self._create_user(email, password, first_name, last_name,  **extra_fields)






class Etablissement (models.Model):
    nom_etablissement =models.CharField(max_length=50)
    adresse_etablissement=models.CharField(max_length=200)  
    logo = models.ImageField(upload_to ='photos/%y/%m/%d' , null=True)
    def __str__(self):
        return self.nom_etablissement

class  Faculté (models.Model):
    nom_faculté =models.CharField(max_length=50)
    adresse_faculté=models.CharField(max_length=200)
    spécialité = models.CharField(max_length=50)
    etablissement = models.ForeignKey( Etablissement ,on_delete=models.CASCADE  )

    def __str__(self):
        return self.nom_faculté

class Département (models.Model) :
    nom_département=models.CharField(max_length=50)
    adresse_département=models.CharField(max_length=200)
    domaine_etude = models.CharField(max_length=50)
    faculté=models.ForeignKey( Faculté ,on_delete=models.CASCADE  )
    
    def __str__(self):
        return self.nom_département


      
class MyAbstractUser(AbstractBaseUser):
  
    email = models.EmailField(verbose_name='email', max_length=60  , unique=True)
    first_name = models.CharField(max_length=30 )
    last_name = models.CharField(max_length=30 )
    etablissement=models.ForeignKey(Etablissement , on_delete=models.CASCADE , null=True )
    numero_telephone =models.CharField( max_length=13,blank=True, help_text='Contact phone number')
    image = models.ImageField(upload_to ='photos/%y/%m/%d' , blank=True, null=True )
    role = models.ManyToManyField(Group,  blank=True )
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name' ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True  

    class Meta:
         abstract=True  
          
         
class MyUser(MyAbstractUser):
    pass
  
    
class Enseignant (MyUser):
    is_professeur = True
    grade= models.CharField(max_length=30 , null=True)
    class Meta :
        verbose_name = 'Professeur'

class Etudiant (MyUser):
    niveau_choice =[
        ('1' , '1er année'), 
        ('2' , '2éme année'),
        ('3' , '3éme année'),
        ('4' , '4éme année'),
        ('5' , '5éme année')

    ]
    num_inscription = models.CharField( primary_key=True ,  max_length=12 ,)
    niveau = models.CharField(max_length=20 , choices=niveau_choice,null=True)
    specialité = models.CharField(max_length=50)
    faculté = models.ForeignKey(Faculté , on_delete=models.CASCADE , default='1')
    departement = models.ForeignKey( Département, on_delete=models.CASCADE , default='1' )
    
    class Meta :
        verbose_name = 'Etudiant'
        

    