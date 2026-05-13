from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns =[
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
    
    path('api/parametre/' , Paramétreview.as_view(), name='parametre'),
    path('api/changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('api/send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('api/reset-password/', UserPasswordResetView.as_view(), name='reset-password'),
    path('api/desactivate-account/', DeactivateUserView.as_view(), name='deactivate-account'),
    path('api/update-picture/', UpdateProfilePictureView.as_view(), name='update-picture'),
    
    path('api/register/invité/', REgistrationInvité.as_view(), name='register-invité'),
    
   
    
    
]+static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)