from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import DonorSignup, Profile, Messages

class DonorSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required, Add a valid email')
    class Meta:
        model = DonorSignup
        fields = ('email', 'username', 'password1', 'password2')

class DonorAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = DonorSignup
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email = email, password = password):
                raise forms.ValidationError("Invalid Login")

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name', 'gender', 'age', 'blood_group', 'phone', 'info']
        widgets = {
            'info': forms.Textarea(attrs={'rows':2, 'cols':23})
        }

class MessageForm(forms.ModelForm):

    class Meta:
        model = Messages
        fields = ['email_to', 'message']
                