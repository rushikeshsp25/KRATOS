from django.contrib.auth.models import Permission, User
from django.db import models
from datetime import datetime

class Debits(models.Model):
    product_name=models.CharField(max_length=250)
    quantity=models.IntegerField(default=0)
    unit=models.CharField(max_length=10,default='NA')   #NA -> Not Applied
    price=models.IntegerField(default=0)
    tax=models.BooleanField(default=0)       #1-GST 0-Not GST

    #systems Fields#############################
    sys_break=models.BooleanField(default=0)
    sys_suspension = models.BooleanField(default=0)
    sys_chasis = models.BooleanField(default=0)
    sys_engine = models.BooleanField(default=0)
    sys_misc = models.BooleanField(default=0)
    ############################################

    category=models.IntegerField(default=0)  #0-other 1-cat1 2-cat2 etc.
    user=models.ForeignKey(User, default=1)
    date_time=models.DateTimeField(default=datetime.now, blank=True)


class Credits(models.Model):
    name_of_payee=models.CharField(max_length=250)
    amount=models.IntegerField(default=0)
    description=models.CharField(max_length=250)
    user = models.ForeignKey(User, default=1) #username who has added this entry
    date_time=models.DateTimeField(default=datetime.now, blank=True)        #system date and time

class Balence(models.Model):
    balence=models.IntegerField()           #Hold current Balence
    '''when amount is credited balence=balence+amount
       when amount is debited balence=balence-amount'''




