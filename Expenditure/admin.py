# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Credits,Debits,Balence,User_info,System,Variables,Category,SubEvent,Event

admin.site.register(Credits)
admin.site.register(Debits)
admin.site.register(Balence)
admin.site.register(User_info)
admin.site.register(System)
admin.site.register(Category)
admin.site.register(SubEvent)
admin.site.register(Event)
admin.site.register(Variables)