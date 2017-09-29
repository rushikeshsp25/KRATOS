from django.contrib.auth.models import Permission, User
from django.db import models
from datetime import datetime

QUANT_CHOICES = (
    ('NA', 'NA'),
    ('Lt', 'Ltr'),
    ('Kg', 'Kg'),
    ('Mt', 'Mtr'),
    ('Gr', 'Gram'),
    ('Ng', 'Nugs'),
)

CAT_CHOICES = (
    ('Other', 'Other'),
    ('Cat1', 'Cat1'),
    ('Cat2', 'Cat2'),
    ('Cat3', 'Cat3'),
)
class Debits(models.Model):
    product_name=models.CharField(max_length=250)
    quantity=models.IntegerField(default=0)
    unit=models.CharField(max_length=10,choices=QUANT_CHOICES,default='NA')  #NA -> Not Applied
    price=models.IntegerField(default=0)
    tax=models.BooleanField()       #1-GST 0-Not GST

    #systems Fields#############################
    sys_break=models.BooleanField()
    sys_suspension = models.BooleanField()
    sys_chasis = models.BooleanField()
    sys_engine = models.BooleanField()
    sys_misc = models.BooleanField()
    ############################################
    category=models.CharField(max_length=10,choices=CAT_CHOICES,default='Other')  #0-other 1-cat1 2-cat2 etc.
    user=models.ForeignKey(User, default=1)
    date_time=models.DateTimeField(default=datetime.now, blank=True)


class Credits(models.Model):
    name_of_payee=models.CharField(max_length=250)
    amount=models.IntegerField(default=0)
    description=models.CharField(max_length=250)
    user = models.ForeignKey(User, default=1) #username who has added this entry
    date_time=models.DateTimeField(default=datetime.now, blank=True)        #system date and time

class Balence(models.Model):
    balence=models.IntegerField()           #id=1 Hold current Balence
                                            #id=2 hold total balence
    '''when amount is credited balence=balence+amount
       when amount is debited balence=balence-amount'''




