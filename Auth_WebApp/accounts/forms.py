from django import forms
from allauth.account.forms import SignupForm as LocalSignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm

# 1. Form for Standard Email/Password Signup
class CustomSignupForm(LocalSignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)
    phone_number = forms.CharField(max_length=15, label='Phone Number', required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.phone_number = self.cleaned_data['phone_number']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = user.email  # Force username = email
        user.save()
        return user

# 2. Form for Google/Social Signup (No Password field)
class CustomSocialSignupForm(SocialSignupForm):
    phone_number = forms.CharField(
        max_length=15, 
        label='Phone Number', 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Required to complete registration'})
    )

    def save(self, request):
        # This 'save' method is called when the user submits the "Almost There" form
        user = super(CustomSocialSignupForm, self).save(request)
        
        # Explicitly save the phone number to the user instance
        user.phone_number = self.cleaned_data['phone_number']
        
        # Ensure username is email (just in case adapter didn't catch it)
        user.username = user.email
        
        user.save()
        return user