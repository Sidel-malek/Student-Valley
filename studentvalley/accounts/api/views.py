from .serializers import *
from accounts.models import *
from rest_framework import generics , status 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from gestion_projet.models import Projet
from django.db.models import Q
from planification.models import Soutenance
from rest_framework.exceptions import ValidationError , APIException




class RegisterAPI(generics.GenericAPIView):
  
    permission_classes = [AllowAny]
    serializer_class = RegisterEtudinatSerializer
    
    def post(self, request ):
        serializer = self.serializer_class(data=request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.data.get('email')
        print(email)
        user = Etudiant.objects.get(email=email)
            
        try:
            projet = Projet.objects.filter(
                Q(membre1_email=email) | Q(membre2_email=email) | Q(membre3_email=email) | Q(membre4_email=email) | Q(membre5_email=email)
            ).first()
        except Projet.DoesNotExist :
            
            if email.endswith("@esi-sba.dz"):
                group = Group.objects.get(name="etudiant")
                user.role.add(group)
                user.save() 
                return Response({'msg': 'Registration successful'}, status=status.HTTP_201_CREATED)
            
            else:
                group = Group.objects.get(name="MembreProjet")
                user.role.add(group)
                user.save()
                return Response({'msg': 'Registration successful'}, status=status.HTTP_201_CREATED)
        
        if projet :
             group = Group.objects.get(name="MembreProjet")
             user.role.add(group)
             user.save()
            
             membres = [
                'membre1',
                'membre2',
                'membre3',
                'membre4',
                'membre5'
              ]
            
        
             for champ in membres:
                    if not getattr(projet, champ):
                        setattr(projet, champ, user)
                        projet.save()
                        break
                
             return Response({'msg': 'Vous avez été enregistré et devenez membre dans le projet "' + projet.theme + '" porté par ' + user.first_name + ' ' + user.last_name}, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_201_CREATED)
        
            
        
               
     
        

      
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response( {"message ": "y3tik sa7a" }, status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            
            return Response( {"message error": "3awdi" } , status=status.HTTP_400_BAD_REQUEST)
        
        

class  Paramétreview (APIView):
  
 # permission_classes = [IsAuthenticated]
  
  def get(self, request):
        try:
            etudiant = Etudiant.objects.get(email='aya2202@gmail.com')
            serializer = ParamétreEtudiantSerializer(etudiant)
            return Response(serializer.data) 
        except Etudiant.DoesNotExist:
            pass
        
        try:
            enseignant = Enseignant.objects.get(email=request.user.email)
            serializer = ParamétreEnseignantSerializer(enseignant)
            return Response(serializer.data) 
        except Enseignant.DoesNotExist:
            pass
        
        
        try:
            user = MyUser.objects.get(email=request.user.email)
            serializer = ParamétreUserSerializer(user)
            return Response(serializer.data) 
        except MyUser.DoesNotExist:
            pass
        
         
        
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    
  def put(self, request):
        try:
            etudiant = Etudiant.objects.get(email=request.user.email)
            serializer = ParamétreEtudiantSerializer(etudiant , data=request.data ,  partial=True)
        except Etudiant.DoesNotExist:
            pass
        
        try:
            enseignant = Enseignant.objects.get(email=request.user.email)
            serializer = ParamétreEnseignantSerializer(enseignant , data=request.data ,   partial=True)
        except Enseignant.DoesNotExist:
            pass
        
        try:
            user = MyUser.objects.get(email=request.user.email)
            serializer = ParamétreUserSerializer(user, data=request.data , partial=True)
        except MyUser.DoesNotExist:
            pass
        
        
        if serializer.is_valid():
          serializer.save()
          return  Response(status=status.HTTP_200_OK, data={"bien modifier"})
        else: 
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"les informations ne sont pas valide"})
         
  
    
class UserChangePasswordView(APIView):
       permission_classes = [IsAuthenticated]
       def post(self, request, uid, token, format=None):
          serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
          serializer.is_valid(raise_exception=True)
          return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

    
class SendPasswordResetEmailView(APIView):
       
       def post(self, request, format=None):
            serializer = SendPasswordResetEmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            if MyUser.objects.filter(email=email).exists():
                user = MyUser.objects.get(email = email)
                random_number = random.randint(100000, 999999)
    
                # Send EMail
                email_user=[user.email , ]
                body = 'enter this following code ' + str(random_number)
                data = {
                    'subject':'Code de Confirmation',
                    'body':body,
                    'to_email':email_user
                 }
      
                Util.send_email(data)
      
      
  
            else:
               raise serializers.ValidationError('You are not a Registered User')
            
            d ={
                'msg':'Password Reset link send. Please check your Email',
                'rendom_number':random_number
             }
            return Response(data=d, status=status.HTTP_200_OK)
 
class UserPasswordResetView(APIView):

  def post(self, request, format=None):
    serializer = UserPasswordResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
 
User = get_user_model()   
    
    
    
class DeactivateUserView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]    
    
    def put(self, request):
    
        user = self.request.user
        
        user.is_active = False
        user.save()
        return Response({"message": "User account deactivated successfully."}, status=status.HTTP_200_OK)
    
    

class UpdateProfilePictureView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfilePictureSerializer

    def get_object(self):
        return self.request.user
    

#############################################################################################################################

class REgistrationInvité(generics.CreateAPIView):
    serializer_class = RegistrationInvitéSerializer
    
    def perform_create(self, serializer):
        group = Group.objects.get(name='Invité')
        email= serializer.validated_data['email']
        try :
            soutenance = Soutenance.objects.get(invité_1_email=email)
        except Soutenance.DoesNotExist :
            return APIException({"message":"vous n'appartient à aucune soutenance"})
        
        super().perform_create(serializer)
        user = serializer.instance
        user.role.add(group)
        user.save()
        soutenance.invité_1= user 
        soutenance.save()
        
        return user
        
    
   
    

        
      
 

      
