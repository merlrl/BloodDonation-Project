from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


# For user registration
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()  # Use the custom user model if available
        fields = ['username', 'email', 'password1', 'password2']  # Include password fields


# For profile creation
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'weight', 'height', 'region', 'province', 'municipality', 'blood_type',
                  'availability', 'last_donation_date']
