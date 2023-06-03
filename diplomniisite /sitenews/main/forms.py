
from django.forms import ModelForm, TextInput
from django.contrib.auth.models import User


class AccountEditForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        widgets = {
            "username": TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя аккаунта'}),
            "email": TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш почтовый ящик'}),
            "first_name": TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            "last_name": TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша фамилия'}),
        }

