from django import forms
from django.contrib.auth.models import User
from .models import Credits,Debits,User_info,Event,SubEvent,System,Category

class DebitsForm(forms.ModelForm):
    CHOICES = [(True, 'GST'),
               (False, 'NON GST')]
    tax = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    users = forms.ModelChoiceField(queryset=User_info.objects.all(),required=False)
    subevents=forms.ModelChoiceField(queryset=SubEvent.objects.all())
    class Meta:
        model = Debits
        fields = ['product_name','quantity','unit','price','tax','system','remarks','category','users','subevents']


class CreditsForm(forms.ModelForm):
    class Meta:
        model = Credits
        fields = ['name_of_payee','amount','description']


class UserForm(forms.ModelForm):
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
        fields = ['username', 'email', 'phone_number','permissions']


class UserMoneyForm(forms.Form):
    user=forms.ModelChoiceField(queryset=User_info.objects.all())
    amount=forms.IntegerField()
    class Meta:
        fields = ['user', 'amount']

class EventForm(forms.ModelForm):
    class Meta:
        model= Event
        fields=['event_name']

class SubeventForm(forms.ModelForm):
    class Meta:
        model= SubEvent
        fields=['subevent_name']

class SystemForm(forms.ModelForm):
    class Meta:
        model= System
        fields=['system_name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model= Category
        fields=['category_name']

class ChangeOngoingEventForm(forms.ModelForm):
    events = forms.ModelChoiceField(queryset=Event.objects.all())
    class Meta:
        model= Event
        fields=['events']