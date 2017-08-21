from django import forms
from django.contrib.auth.models import User

from .models import Debits
from .models import Credits,Debits

class DebitsForm(forms.ModelForm):

    class Meta:
        model = Debits
        fields = ['product_name']


class CreditsForm(forms.ModelForm):
    description=forms.CharField(required=False)
    class Meta:
        model = Credits
        fields = ['name_of_payee','amount','description']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
