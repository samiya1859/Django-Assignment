from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm                                 
from django import forms
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')
    user_type = forms.ChoiceField(choices=Profile.USER_TYPES, label="User Type")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        # Save the User object
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False  # Initially inactive, to be activated by admin

        if commit:
            user.save()

        # Save the Profile object
        profile = Profile(user=user, user_type=self.cleaned_data['user_type'])
        profile.save()

        return user
    
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-input w-full p-2 border border-gray-300 rounded-md', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input w-full p-2 border border-gray-300 rounded-md', 'placeholder': 'Password'})
    )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

        