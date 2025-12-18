from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# Registration Form
class RegistrationForm( UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=150, required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = CustomUser
        fields = ["username", "full_name", "email", "phone", "password1", "password2"]

    # Example: custom email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email

    # Example: custom password length validation
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")
        if len(password) > 50:
            raise forms.ValidationError("Password cannot exceed 50 characters.")
        return password
# Login Form
class LoginForm(forms.Form):
    email = forms.EmailField()

# OTP Verification Form
class VerifyForm(forms.Form):
    otp = forms.CharField(max_length=6)
