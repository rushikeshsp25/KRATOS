from django import forms
from django.contrib.auth.models import User
from .models import Credits,Debits

class DebitsForm(forms.ModelForm):
    CHOICES = [(True, 'GST'),
               (False, 'NON GST')]

    tax = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Debits
        fields = ['product_name','quantity','unit','price','tax','sys_break','sys_suspension',
                  'sys_chasis','sys_engine','sys_misc','category']


class CreditsForm(forms.ModelForm):
    description=forms.CharField(required=False)
    class Meta:
        model = Credits
        fields = ['name_of_payee','amount','description']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
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
        fields = ['username', 'email', 'password','permissions']


