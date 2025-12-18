from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    email = forms.EmailField()

class VerifyForm(forms.Form):
    otp = forms.CharField(max_length=6)