from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render,redirect, get_object_or_404
from .forms import UserForm,CreditsForm,DebitsForm
from .models import Credits,Debits,Balence
from django.db.models import Q
from datetime import datetime,date      #to get current date and time

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'Expenditure/login.html')
    else:
        #for todays debits gauge
        d_objs = Debits.objects.filter(date_time__contains=date.today())
        todays_expenditure = 0
        for obj in d_objs:
            todays_expenditure = todays_expenditure + obj.price
        #for todays credits gauge
        c_objs = Credits.objects.filter(date_time__contains=date.today())
        todays_credits = 0
        for obj in c_objs:
            todays_credits = todays_credits + obj.amount

        #for displaying tax donut
        price_gst=0
        price_non_gst=0
        price_cat1, price_cat2, price_cat3,price_other = 0,0,0,0
        d_objs = Debits.objects.all()
        for obj in d_objs:
            if obj.tax == True:
                price_gst = price_gst + obj.price
            else:
                price_non_gst=price_non_gst+ obj.price
            if obj.category== "Cat1":
                price_cat1+=obj.price
            elif obj.category== "Cat2":
                price_cat2+=obj.price
            elif obj.category== "Cat3":
                price_cat3+=obj.price
            else:
                price_other+=obj.price


        #for passing objects to js we need to serialize it
        json_data=serializers.serialize("json",Balence.objects.all())

        context = {
            "json": json_data,
            "todays_expenditure":todays_expenditure,
            "todays_credits":todays_credits,
            "price_gst":price_gst,
            "price_non_gst":price_non_gst,
            "price_cat1":price_cat1,
            "price_cat2":price_cat2,
            "price_cat3":price_cat3,
            "price_other":price_other,
        }
        return render(request, 'Expenditure/Dashboard.html',context)


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
                return render(request, 'Expenditure/Dashboard.html')
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
            #display Model User Succesfully Created
            return render(request, 'Expenditure/success.html')
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
            bal1=Balence.objects.get(id=1)
            bal2 = Balence.objects.get(id=2)
            bal1.balence=bal1.balence+credit.amount
            bal2.balence = bal2.balence + credit.amount
            bal1.save()
            bal2.save()
            return render(request, 'Expenditure/success.html')

        credits_object=Credits.objects.order_by('-date_time')[:5]

        context = {
            "form": form,
            "credits":credits_object,
            "balence":Balence.objects.get(id=1),
        }
        return render(request, 'Expenditure/credit_form.html', context)
    else:
        return render(request, 'Expenditure/login.html')


def debits(request):
    if request.user.is_authenticated():
        form = DebitsForm(request.POST or None)
        if form.is_valid():
            debit=form.save(commit=False)
            debit.user=request.user
            debit.save()
            bal = Balence.objects.get(id=1)
            bal.balence = bal.balence - debit.price
            bal.save()
            return render(request, 'Expenditure/success.html')
        debits_object = Debits.objects.order_by('-date_time')[:10]
        context = {
            "form": form,
            "debits":debits_object,
        }
        return render(request, 'Expenditure/debit_form.html',context)
    else:
        return render(request, 'Expenditure/login.html')

def reports(request):
    if request.user.is_authenticated():
        return render(request, 'Expenditure/reports.html')
    else:
        return render(request, 'Expenditure/login.html')

def report_engine(request):
    if request.user.is_authenticated():
        report_type="System Wise Report"
        report_desc="System - Engine"
        d_objs = Debits.objects.filter(sys_engine=1).order_by('-date_time')
        context={
            "report_type":report_type,
            "report_desc":report_desc,
            "debits":d_objs,
        }
        return render(request, 'Expenditure/report_result.html',context)
    else:
        return render(request, 'Expenditure/login.html')

