from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from .forms import UserForm,CreditsForm,DebitsForm
from .models import Credits,Debits
from django.db.models import Q
from datetime import datetime       #to get current date and time

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'Expenditure/login.html')
    else:
        return render(request, 'Expenditure/index.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'Expenditure/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'Expenditure/index.html')
            else:
                return render(request, 'Expenditure/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'Expenditure/login.html', {'error_message': 'Invalid login'})
    return render(request, 'Expenditure/login.html')

def create_new_user(request):
    if request.user.is_authenticated():
        form = UserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'Expenditure/index.html')
        context = {
            "form": form,
        }
        return render(request, 'Expenditure/create_new_user.html', context)
    else:
        return render(request, 'Expenditure/login.html')


def credits(request):
    if request.user.is_authenticated():
        form = CreditsForm(request.POST or None)
        if form.is_valid():
            credit=form.save(commit=False)
            credit.user=request.user
            credit.save()
            return render(request, 'Expenditure/success.html')
        #pk=Credits.objects.latest('id').id
        credits_object=Credits.objects.order_by('-date_time')[:5]

        context = {
            "form": form,
            "credits":credits_object,
        }
        return render(request, 'Expenditure/credit_form.html', context)
    else:
        return render(request, 'Expenditure/login.html')


def debits(request):
    if request.user.is_authenticated():
        form = DebitsForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, 'Expenditure/debit_form.html',context)
    else:
        return render(request, 'Expenditure/login.html')