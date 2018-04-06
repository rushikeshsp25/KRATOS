from django.contrib.auth.models import Permission, User
from django.db import models
from django.utils.timezone import now

QUANT_CHOICES = (
    ('NA', 'NA'),
    ('Lt', 'Ltr'),
    ('Kg', 'Kg'),
    ('Mt', 'Mtr'),
    ('Gr', 'Gram'),
    ('Ng', 'Nugs'),
)

class Category(models.Model):
    category_name=models.CharField(max_length=16,unique=True)
    def __str__(self):
        return self.category_name

class System(models.Model):
    system_name=models.CharField(max_length=16,unique=True)
    def __str__(self):
        return self.system_name

class Event(models.Model):
    event_name=models.CharField(max_length=20,unique=True)
    date_time = models.DateTimeField(default=now, blank=True)
    def __str__(self):
        return self.event_name

class SubEvent(models.Model):
    subevent_name=models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.subevent_name

class Variables(models.Model):
    name=models.CharField(max_length=20,unique=True)
    value=models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Debits(models.Model):
    product_name=models.CharField(max_length=250)
    quantity=models.IntegerField()
    unit=models.CharField(max_length=10,choices=QUANT_CHOICES,default='NA')  #NA -> Not Applied
    price=models.IntegerField()
    tax=models.BooleanField()       #1-GST 0-Not GST
    #systems Fields#############################
    system=models.ForeignKey(System,default=1)
    ############################################
    remarks=models.TextField(blank=True)
    category=models.ForeignKey(Category,default=1)
    user=models.ForeignKey(User)
    event = models.ForeignKey(Event)
    subevent=models.ForeignKey(SubEvent,default=1)
    date_time=models.DateTimeField(default=now, blank=True)


class Credits(models.Model):
    name_of_payee=models.CharField(max_length=250)
    amount=models.IntegerField(default=0)
    description=models.TextField(blank=True)
    user = models.ForeignKey(User, default=1) #username who has added this entry
    event = models.ForeignKey(Event)
    date_time=models.DateTimeField(default=now, blank=True)        #system date and time

class Balence(models.Model):
    total_balence=models.IntegerField()
    current_balence=models.IntegerField()
    event=models.ForeignKey(Event, default=1)
    #balence=models.IntegerField()           #id=1 Hold current Balence
                                            #id=2 hold total balence
    '''when amount is credited balence=balence+amount
       when amount is debited balence=balence-amount'''

class User_info(models.Model):
    user = models.ForeignKey(User, default=1)
    phone_number = models.CharField(max_length=16)  # validators should be a list
    assets=models.IntegerField()
    def __str__(self):
        return self.user.username





