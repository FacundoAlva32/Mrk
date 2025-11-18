from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    
    def populate_user(self, request, sociallogin, data):
        """
        Personaliza cómo se crean los usuarios de redes sociales
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Para usuarios de Google
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            
            # Usar el email como username si no hay username
            if not user.username and user.email:
                user.username = user.email.split('@')[0]
            
            # Llenar nombre y apellido desde Google
            if extra_data.get('given_name'):
                user.first_name = extra_data.get('given_name', '')
            if extra_data.get('family_name'):
                user.last_name = extra_data.get('family_name', '')
                
        return user