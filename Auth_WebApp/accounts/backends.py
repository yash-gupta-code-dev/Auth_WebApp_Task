from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailPhoneUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None
        
        try:
            # Attempt to find user by any of the 3 fields
            user = User.objects.get(
                Q(username__iexact=username) | 
                Q(email__iexact=username) | 
                Q(phone_number__iexact=username)
            )
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # Safety net for duplicates
            user = User.objects.filter(
                Q(username__iexact=username) | 
                Q(email__iexact=username) | 
                Q(phone_number__iexact=username)
            ).order_by('id').first()
        except Exception as e:
            # CRITICAL: Print the error to terminal so we know why it crashed
            print(f"Error in EmailPhoneUsernameBackend: {e}")
            return None

        # Check password
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None