from __future__ import print_function
from django.contrib.auth import authenticate, login,logout
from django.core import serializers
from django.shortcuts import render, redirect ,get_object_or_404
from .forms import UserForm, CreditsForm, DebitsForm,UserMoneyForm,EventForm,SubeventForm,SystemForm,CategoryForm,ChangeOngoingEventForm
from .models import Credits, Debits, Balence, User_info,System,Category,Event,SubEvent,Variables
from datetime import date  # to get current date and time
from django.contrib.auth.models import User,Group
import csv
import re
from django.http import HttpResponse
from django.http import JsonResponse
import json as simplejson
import random
from django.core.mail import send_mail
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('Expenditure:index')  # redirect() accepts a view name as parameter
            else:
                return render(request, 'Expenditure/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'Expenditure/login.html', {'error_message': 'Invalid login'})
    return render(request, 'Expenditure/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'Expenditure/login.html', context)



def create_new_user(request):
    if request.user.is_authenticated():
        if request.user.has_perm('Expenditure.add_User'):
            form = UserForm(request.POST or None)
            if form.is_valid():
                user = form.save(commit=False)
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                if email and User.objects.get(email=email).count() > 0:
                    context = {
                        'error_message': 'This email address is already registered.',
                        "form": form,
                    }
                    return render(request, 'Expenditure/create_new_user.html', context)
                password = str(random.randint(1000,9999))
                user.set_password(password)
                user_info_object = User_info()
                pattern = re.compile("^[789]\d{9}$")
                user_info_object.phone_number = request.POST['phone_number']  # before saving user validate phone_number
                if not pattern.match(str(user_info_object.phone_number)):
                    context = {
                        'error_message': 'Enter 10 Digit Mobile Number in Proper Format',
                        "form": form,
                    }
                    return render(request, 'Expenditure/create_new_user.html', context)
                email_body="Hello,Your account is created on KratosWebApp by "+str(request.user.username)+"\nYour Credentials\n"+"Username:- "+str(username)+"\n"+"Password:- "+str(password)+"\n"+"Do not share your credentials.\n"
                try:
                    send_mail('Your account is created on KratosWebApp', email_body, 'noreply@parsifal.co', [email])
                except Exception as e:
                    messages.error(request, 'It seems that your network is not supporting SMTP, Try on different Network !')
                else:
                    user.save()
                    user_info_object.user = user
                    user_info_object.assets = 0
                    user_info_object.save()
                    g = Group.objects.get(name=str(form.cleaned_data['permissions']))
                    g.user_set.add(user)
                    messages.success(request, 'New User is successfully created !')
            context = {
                "form": form,
                "ongoing_event":Variables.objects.get(name="ongoing_event"),
            }
            return render(request, 'Expenditure/create_new_user.html', context)
        else:
            return render(request, 'Expenditure/permission_error.html')
    else:
        return render(request, 'Expenditure/login.html')

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'Expenditure/login.html')
    else:
        event_obj=Event.objects.all()
        subevent_obj=SubEvent.objects.all()
        system_obj=System.objects.all()
        category_obj=Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:       #means is no event is created yet
            return redirect('Expenditure:account')

        # for todays debits gauge
        d_objs = Debits.objects.filter(date_time__contains=date.today())
        d_objs=d_objs.filter(event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
        todays_expenditure = 0
        for obj in d_objs:
            todays_expenditure = todays_expenditure + obj.price
        # for todays credits gauge
        c_objs = Credits.objects.filter(date_time__contains=date.today())
        c_objs=c_objs.filter(event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
        todays_credits = 0
        for obj in c_objs:
            todays_credits = todays_credits + obj.amount

        # for displaying tax donut
        price_gst = 0
        price_non_gst = 0
        d_objs = Debits.objects.filter(event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
        c_objs = Credits.objects.filter(
            event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
        for obj in d_objs:
            if obj.tax == True:
                price_gst = price_gst + obj.price
            else:
                price_non_gst = price_non_gst + obj.price

        # for passing objects to js we need to serialize it
        # json_data = serializers.serialize("json", Balence.objects.all())
        bal=Balence.objects.get(event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
        total_balence=bal.total_balence
        current_balence = bal.current_balence
        debits_object = d_objs.order_by('-date_time')[:2]   #for displaying recent 2 debits and credits
        credits_object = c_objs.order_by('-date_time')[:2]
        categories=Category.objects.all()
        categories_amount={}
        for category in categories:
            deb_objs=d_objs.filter(category=category)
            amount=0
            for deb in deb_objs:
                amount=amount+deb.price
            categories_amount[category.category_name]=amount
        json_categories_amount=simplejson.dumps(categories_amount)

        systems = System.objects.all()
        system_amount = {}
        for system in systems:
            deb_objs = d_objs.filter(system=system)
            amount = 0
            for deb in deb_objs:
                amount = amount + deb.price
            system_amount[system.system_name] = amount
        json_system_amount = simplejson.dumps(system_amount)

        context = {
            "json_categories_amount":json_categories_amount,
            "json_system_amount":json_system_amount,
            "current_balence":current_balence,
            "total_balence":total_balence,
            "todays_expenditure": todays_expenditure,
            "todays_credits": todays_credits,
            "price_gst": price_gst,
            "price_non_gst": price_non_gst,
            "credits":credits_object,
            "debits":debits_object,
            "ongoing_event": Variables.objects.get(name="ongoing_event"),
        }
        return render(request, 'Expenditure/Dashboard.html', context)

def credits(request):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj = System.objects.all()
        category_obj = Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:  # means is no event is created yet
            return redirect('Expenditure:account')

        if not request.user.has_perm('Expenditure.add_Credits'):
            return render(request, 'Expenditure/permission_error.html')

        form = CreditsForm(request.POST or None)
        if form.is_valid():
            credit = form.save(commit=False)
            credit.user = request.user
            credit.event = Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value)
            credit.save()
            bal = Balence.objects.get(
                event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
            bal.total_balence = bal.total_balence + credit.amount
            bal.current_balence = bal.current_balence + credit.amount
            bal.save()
            messages.success(request, 'Credit is successfully added!')
            return redirect('Expenditure:credits')

        credits_object = Credits.objects.filter(event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
        credits_object=credits_object.order_by('-date_time')[:5]

        context = {
            "form": form,
            "credits": credits_object,
            "balence":Balence.objects.get(event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
,
            "ongoing_event": Variables.objects.get(name="ongoing_event"),
        }
        return render(request, 'Expenditure/credit_form.html', context)
    else:
        return render(request, 'Expenditure/login.html')

def edit_credit(request,id):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj = System.objects.all()
        category_obj = Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:  # means is no event is created yet
            return redirect('Expenditure:account')

        if not request.user.has_perm('Expenditure.add_Debits'):
            return render(request, 'Expenditure/permission_error.html')

        item = get_object_or_404(Credits, pk=id)
        form = CreditsForm(request.POST or None,instance=item)
        if form.is_valid():
            credit = form.save(commit=False)
            credit.user = request.user
            credit.save()
            bal = Balence.objects.get(
                event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
            bal.total_balence = bal.total_balence + credit.amount
            bal.current_balence = bal.current_balence + credit.amount
            bal.save()
            messages.success(request, 'Changes to Credits are successfully saved!')
            return redirect('Expenditure:credits')
        credits_object = Credits.objects.filter(
            event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
        credits_object = credits_object.order_by('-date_time')[:5]
        context = {
                "form": form,
                "credits": credits_object,
                "balence":Balence.objects.get(event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
,
            "ongoing_event": Variables.objects.get(name="ongoing_event"),
            }
        return render(request, 'Expenditure/credit_form.html', context)
    else:
        return render(request, 'Expenditure/login.html')


def delete_credit(request, oid):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj = System.objects.all()
        category_obj = Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:  # means is no event is created yet
            return redirect('Expenditure:account')

        if not request.user.has_perm('Expenditure.delete_Credits'):
            return render(request, 'Expenditure/permission_error.html')

        c_obj=Credits.objects.get(pk=int(oid))
        bal=Balence.objects.get(event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
        bal.total_balence=bal.total_balence-c_obj.amount
        bal.current_balence = bal.current_balence-c_obj.amount
        bal.save()
        c_obj.delete()
        messages.success(request, 'Credit is deleted Successfully!')
        return redirect('Expenditure:credits')
    else:
        return render(request, 'Expenditure/login.html')

def debits(request):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj = System.objects.all()
        category_obj = Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:  # means is no event is created yet
            return redirect('Expenditure:account')

        if not request.user.has_perm('Expenditure.add_Debits'):
            return render(request, 'Expenditure/permission_error.html')

        form = DebitsForm(request.POST or None)
        if form.is_valid():
            debit = form.save(commit=False)
            debit.user = request.user
            debit.event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value)
            debit.save()
            bal = Balence.objects.get(
            event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
            bal.current_balence = bal.current_balence - debit.price
            bal.save()
            username = form.cleaned_data['users']
            if username:
                user = get_object_or_404(User_info, user=User.objects.get(username=username))
                user.assets = user.assets + debit.price
                user.save()
            messages.success(request, 'Debit is successfully added!')
            return redirect('Expenditure:debits')
        debits_object = Debits.objects.filter(
            event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
        debits_object = debits_object.order_by('-date_time')[:10]
        context = {
            "form": form,
            "debits": debits_object,
            "ongoing_event": Variables.objects.get(name="ongoing_event"),
        }
        return render(request, 'Expenditure/debit_form.html', context)
    else:
        return render(request, 'Expenditure/login.html')

def edit_debit(request,id):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj = System.objects.all()
        category_obj = Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:  # means is no event is created yet
            return redirect('Expenditure:account')
        if request.user.has_perm('Expenditure.change_Debits'):
            item = get_object_or_404(Debits, pk=id)
            form = DebitsForm(request.POST or None, instance=item)
            if form.is_valid():
                debit = form.save(commit=False)
                debit.user = request.user
                item = get_object_or_404(Debits, pk=id)
                debit.save()
                bal = Balence.objects.get(
                event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
                bal.current_balence = bal.current_balence + item.price
                bal.current_balence = bal.current_balence - debit.price
                bal.save()
                username = form.cleaned_data['users']
                user = get_object_or_404(User_info, user=User.objects.get(username=username))
                user.assets = user.assets - item.price
                user.assets = user.assets + debit.price
                user.save()
                messages.success(request, 'Changes are successfully saved!')
                return redirect('Expenditure:debits')
            debits_object = Debits.objects.filter(
                event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))
            debits_object = debits_object.order_by('-date_time')[:10]
            context = {
                "form": form,
                "debits": debits_object,
                "ongoing_event": Variables.objects.get(name="ongoing_event"),
            }
            return render(request, 'Expenditure/debit_form.html', context)
        else:
            return render(request, 'Expenditure/permission_error.html')

    else:
        return render(request, 'Expenditure/login.html')


def delete_debit(request, oid):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj = System.objects.all()
        category_obj = Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:  # means is no event is created yet
            return redirect('Expenditure:account')
        if request.user.has_perm('Expenditure.delete_Debits'):
            d_obj=Debits.objects.get(pk=int(oid))
            bal = Balence.objects.get(
                event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))

            bal.current_balence=bal.current_balence+d_obj.price
            bal.save()
            d_obj.delete()
            messages.success(request, 'Debit is Deleted Successfully !')
            return redirect('Expenditure:debits')
        else:
            return render(request, 'Expenditure/permission_error.html')

    else:
        return render(request, 'Expenditure/login.html')

def users(request):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj = System.objects.all()
        category_obj = Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:  # means is no event is created yet
            return redirect('Expenditure:account')
        users_objects=User_info.objects.all()
        context={
            "users":users_objects,
            "ongoing_event": Variables.objects.get(name="ongoing_event"),
        }
        return render(request, 'Expenditure/users.html',context)
    else:
        return render(request, 'Expenditure/login.html')

def reports(request):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj = System.objects.all()
        category_obj = Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:  # means is no event is created yet
            return redirect('Expenditure:account')
        systems=System.objects.all()
        categories=Category.objects.all()
        context={
            "systems":systems,
            "categories":categories,
            "ongoing_event": Variables.objects.get(name="ongoing_event"),
        }
        return render(request, 'Expenditure/reports.html',context)
    else:
        return render(request, 'Expenditure/login.html')


def report_result(request, type, subtype):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj = System.objects.all()
        category_obj = Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:  # means is no event is created yet
            return redirect('Expenditure:account')
        report_type = ""
        report_desc = ""
        cord=0      # c or d , 0 if credits object 1 if debits object
        objs=None

        if type == 'systemwise':
            cord=1
            report_type = "System Wise Report"
            report_desc = "System - "+subtype
            objs = Debits.objects.filter(system__system_name=subtype).order_by('-date_time')

        elif type == "categorywise":
            cord=1
            report_type = "Category Wise Report"
            report_desc = "Category -"+subtype
            objs = Debits.objects.filter(category__category_name=subtype).order_by('-date_time')

        elif type=="credits" and subtype=='all':
            cord=0
            report_type = "Credits Report"
            report_desc = ""
            objs = Credits.objects.all().order_by('-date_time')

        elif type=="debits" and subtype=='all':
            cord=1
            report_type = "Debits Report"
            report_desc = ""
            objs = Debits.objects.all().order_by('-date_time')

        objs = objs.filter(event=Event.objects.get(event_name=Variables.objects.get(name="ongoing_event").value))

        context = {
            "cord":cord,
            "report_type": report_type,
            "report_desc": report_desc,
            "objs": objs,
            "ongoing_event": Variables.objects.get(name="ongoing_event"),
        }

        return render(request, 'Expenditure/report_result.html', context)
    else:
        return render(request, 'Expenditure/login.html')



def export_csv(request,type):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj = System.objects.all()
        category_obj = Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:  # means is no event is created yet
            return redirect('Expenditure:account')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        head_row=[]
        objects=[]
        if(type=="credits"):
            head_row = ['name_of_payee', 'amount', 'description', 'user', 'date_time']
            objects = Credits.objects.all().values_list('name_of_payee', 'amount', 'description', 'user', 'date_time')
        elif(type=="debits"):
            head_row = ['product_name', 'quantity', 'unit', 'price', 'tax','remarks','category','user','date_time']
            objects = Debits.objects.all().values_list('product_name', 'quantity', 'unit', 'price', 'tax','remarks','category','user','date_time')
        writer = csv.writer(response)
        writer.writerow(head_row)
        for object in objects:
            writer.writerow(object)
        return response
    else:
        return render(request, 'Expenditure/login.html')

def issue_money_to_user(request):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj = System.objects.all()
        category_obj = Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:  # means is no event is created yet
            return redirect('Expenditure:account')
        if not request.user.has_perm('Expenditure.change_User_info') or not request.user.has_perm('Expenditure.add_User_info'):
            return render(request, 'Expenditure/permission_error.html')

        form = UserMoneyForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['user']
            assets=form.cleaned_data['amount']
            user = get_object_or_404(User_info,user=User.objects.get(username=username))
            user.assets=user.assets-assets
            user.save()
            messages.success(request, 'Amount is successfully added to ' + user.user.username + "'s assets !")
            return redirect('Expenditure:issue_money_to_user')
        context = {
            "form": form,
            "ongoing_event": Variables.objects.get(name="ongoing_event"),
        }
        return render(request, 'Expenditure/issue_money_to_user.html', context)

    else:
        return render(request, 'Expenditure/login.html')

def receive_money_from_user(request):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj = System.objects.all()
        category_obj = Category.objects.all()
        if not event_obj or not subevent_obj or not system_obj or not category_obj:  # means is no event is created yet
            return redirect('Expenditure:account')

        if not request.user.has_perm('Expenditure.add_User_info') or not request.user.has_perm('Expenditure.change_User_info'):
            return render(request, 'Expenditure/permission_error.html')

        form = UserMoneyForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['user']
            assets=form.cleaned_data['amount']
            user = get_object_or_404(User_info,user=User.objects.get(username=username))
            user.assets=user.assets+assets
            user.save()
            messages.success(request, 'Amount is successfully deducted from ' + user.user.username + "'s assets !")
            return redirect('Expenditure:receive_money_from_user')
        context = {
            "form": form,
            "ongoing_event": Variables.objects.get(name="ongoing_event"),
        }
        return render(request, 'Expenditure/receive_money_from_user.html', context)

    else:
        return render(request, 'Expenditure/login.html')


def account(request):
    if request.user.is_authenticated():
        error=""
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()
        system_obj=System.objects.all()
        category_obj=Category.objects.all()
        user_obj=None
        ongoing_event=None
        if not event_obj and not subevent_obj and not system_obj and not category_obj:  # means is no event is created yet
            error="You need to create Atleast One Event, One Subevent, One System and One Category to Enter System !!"
        else:
            if not event_obj:  # means is no event is created yet
                error=error+"You need to create Atleast One Event to Enter System !!\n"
            if not subevent_obj:  # means is no event is created yet
                error=error+"You need to create Atleast One Subevent to Enter System !!\n"
            if not system_obj:  # means is no event is created yet
                error=error+"You need to create Atleast One System to Enter System !!\n"
            if not category_obj:  # means is no event is created yet
                error=error+"You need to create Atleast One Category to Enter System !!\n"
        try:
            user_obj=User_info.objects.get(user=request.user)
        except:
            user_obj=None
        eventForm=EventForm(request.POST or None)
        subeventForm = SubeventForm(request.POST or None)
        systemForm=SystemForm(request.POST or None)
        categoryForm=CategoryForm(request.POST or None)
        changeongoingeventForm = ChangeOngoingEventForm(request.POST or None)
        try:
            ongoing_event=Variables.objects.get(name="ongoing_event")
        except:
            ongoing_event=None
        context= {
                 "user_obj":user_obj,
                 "eventForm":eventForm,
                 "subeventForm":subeventForm,
                 "error":error,
                 "ongoing_event": ongoing_event,
                 "systemForm":systemForm,
                  "categoryForm":categoryForm,
                  "changeongoingeventForm":changeongoingeventForm,
                 }
        return render(request,'Expenditure/account.html',context)
    else:
        return render(request, 'Expenditure/login.html')

def add_event(request):
    if request.user.is_authenticated():
        if not request.user.has_perm('Expenditure.add_Event'):
            return render(request, 'Expenditure/permission_error.html')

        eventForm = EventForm(request.POST or None)
        changeongoingeventForm = ChangeOngoingEventForm(request.POST or None)
        if eventForm.is_valid():
            eventname = eventForm.cleaned_data['event_name']
            event=Event()
            event.event_name=eventname
            event.save()

            try:
                ongoing_event=Variables.objects.get(name="ongoing_event")
                ongoing_event.value=eventname
                ongoing_event.save()
            except:
                var=Variables()
                var.name="ongoing_event"
                var.value=eventname
                var.save()

            bal=Balence()
            bal.total_balence=0
            bal.current_balence=0
            bal.event=event
            bal.save()
            #request.session['Event'] =event
            return render(request, 'Expenditure/new_event_created.html',{"event":event,
                                                                         "changeongoingeventForm":changeongoingeventForm,
                                                                         })
        return redirect('Expenditure:account')

    else:
        return render(request, 'Expenditure/login.html')

def add_subevent(request):
    if request.user.is_authenticated():
        event_obj = Event.objects.all()
        subevent_obj = SubEvent.objects.all()

        if not request.user.has_perm('Expenditure.add_Subevent'):
            return render(request, 'Expenditure/permission_error.html')

        subeventForm = SubeventForm(request.POST or None)
        if subeventForm.is_valid():
            subeventname = subeventForm.cleaned_data['subevent_name']
            subevent=SubEvent()
            subevent.subevent_name=subeventname
            subevent.save()
            messages.success(request, 'New Subevent is successfully Created !')
        return redirect('Expenditure:account')


    else:
        return render(request, 'Expenditure/login.html')

def add_system(request):
    if request.user.is_authenticated():
        if not request.user.has_perm('Expenditure.add_System'):
            return render(request, 'Expenditure/permission_error.html')

        systemForm = SystemForm(request.POST or None)
        if systemForm.is_valid():
            systemname = systemForm.cleaned_data['system_name']
            system=System()
            system.system_name=systemname
            system.save()
            messages.success(request,'New System is successfully Created !')
        return redirect('Expenditure:account')

    else:
        return render(request, 'Expenditure/login.html')

def add_category(request):
    if request.user.is_authenticated():
        if not request.user.has_perm('Expenditure.add_Category'):
            return render(request, 'Expenditure/permission_error.html')

        categoryForm = CategoryForm(request.POST or None)
        if categoryForm.is_valid():
            categoryname = categoryForm.cleaned_data['category_name']
            category=Category()
            category.category_name=categoryname
            category.save()
            messages.success(request, 'New Category is successfully Created !')
        return redirect('Expenditure:account')

    else:
        return render(request, 'Expenditure/login.html')

def change_ongoing_event(request):
    if request.user.is_authenticated():
        if not request.user.has_perm('Expenditure.change_Variables'):
            return render(request, 'Expenditure/permission_error.html')

        changeongoingeventForm = ChangeOngoingEventForm(request.POST or None)
        if changeongoingeventForm.is_valid():
            eventname = changeongoingeventForm.cleaned_data['events']
            ongoing_event=Variables.objects.get(name="ongoing_event")
            ongoing_event.value=str(eventname)
            ongoing_event.save()
            messages.success(request, 'Ongoing event is successfully set to '+str(eventname))
        return redirect('Expenditure:account')

    else:
        return render(request, 'Expenditure/login.html')

def autocomplete(request):
    if request.is_ajax():
        queryset = Debits.objects.filter(product_name__startswith=request.GET.get('search', None))
        list = []
        for i in queryset:
            list.append(i.product_name)
        data = {
            'list': list,
        }
        return JsonResponse(data)