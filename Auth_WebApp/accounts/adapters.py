# accounts/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_field

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        """
        Hook that populates the user instance with data from the provider.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Force the username to be the email address
        if user.email:
            user_field(user, 'username', user.email)
            
        return user