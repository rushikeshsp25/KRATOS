# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Credits,Debits

admin.site.register(Credits)
admin.site.register(Debits)


