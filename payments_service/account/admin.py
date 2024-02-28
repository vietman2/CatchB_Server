from django.contrib import admin

from .models import BankAccount, Bank

admin.site.register(BankAccount)
admin.site.register(Bank)
