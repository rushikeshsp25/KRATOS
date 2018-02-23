from django import forms
from django.contrib.auth.models import User
from .models import Credits,Debits,User_info

class DebitsForm(forms.ModelForm):
    CHOICES = [(True, 'GST'),
               (False, 'NON GST')]
    tax = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = Debits
        fields = ['product_name','quantity','unit','price','tax','system','remarks','category']


class CreditsForm(forms.ModelForm):
    class Meta:
        model = Credits
        fields = ['name_of_payee','amount','description']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone_number=forms.CharField(max_length=16)
    group_choises = (
        ('view', 'view'),
        ( 'view_add','view + add'),
        ( 'view_add_edit','view + add + edit'),
        ( 'view_add_edit_delete','view + add + edit + delete'),
        ('superuser', 'superuser'),
    )

    permissions = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect(),
        choices=group_choises,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number','password','permissions']


class UserMoneyForm(forms.Form):
    user=forms.ModelChoiceField(queryset=User_info.objects.all())
    amount=forms.IntegerField()
    class Meta:
        fields = ['user', 'amount']