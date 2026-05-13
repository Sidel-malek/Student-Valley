from django.contrib import admin 
from .models import *

from django.contrib.auth.admin import UserAdmin
from django.template.loader import render_to_string
from .models import MyUser
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Register your models here.

class MyUserAdmin(admin.ModelAdmin):
    list_display = ( 'email', 'first_name', 'last_name',  'etablissement', 'is_active' , 'is_staff')
    list_filter = ('is_admin', )

    fieldsets=(
        (None , {'fields' : ('email', 'password', 'first_name', 'last_name' , 'etablissement', 'image' , 'numero_telephone', 'role')}), 
        ('permissions', {'fields' :('is_admin', 'is_staff' , 'is_active')})
    )
    add_fieldsets= (
        ( None , {
               'classes': ('wide', ), 
               'fields' : ('email' ,'password1', 'password2' ), 
        }
        
        )
    )

    search_fields =( 'role__name','email' , )
    ordering= ('email', )
    filter_horizontal=()

    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password) # hash the password
        super().save_model(request, obj, form, change)


admin.site.register(MyUser , MyUserAdmin)

class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ( 'email', 'first_name', 'last_name', 'is_active' , 'is_staff')
    list_filter = ('is_admin', )

    fieldsets=(
        (None , {'fields' : ('email', 'password', 'first_name', 'last_name' ,'grade' , 'etablissement' , 'role' , 'image')}), 
        ('Permissions', {'fields' :('is_admin', 'is_staff' , 'is_active')})
    )
    add_fieldsets= (
        ( None , {
               'classes': ('wide', ), 
               'fields' : ('email' ,'password1', 'password2' ), 
        }
        
        )
    )

    search_fields =('email','role' )
    ordering= ('email', )
    filter_horizontal=()

   
    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password) # hash the password
        super().save_model(request, obj, form, change)

admin.site.register(Enseignant , ProfesseurAdmin)



class EtudiantAdmin(admin.ModelAdmin):
    list_display = (  'email', 'first_name', 'last_name' ,'is_active' , 'is_staff' )
   

    fieldsets=(
        (None , {'fields' : ('email' ,'num_inscription', 'niveau'  , 'role','image')}), 
    
    )
    add_fieldsets= (
        ( None , {
               'classes': ('wide', ), 
               'fields' : ('email' ,'password1', 'password2' ), 
        }
        
        )
    )

    search_fields =('email', )
    ordering= ('email', )
    filter_horizontal=()

    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password) # hash the password
        super().save_model(request, obj, form, change)
admin.site.register(Etudiant, EtudiantAdmin)


admin.site.register(Etablissement)
admin.site.register(Département)
admin.site.register(Faculté)



