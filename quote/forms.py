from django import forms
from .models import Quote
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Nie podajemy user, bo przypiszemy go automatycznie w widoku (request.user)
class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['author', 'text', 'category']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']