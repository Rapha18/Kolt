from django.contrib import admin
from .models import CustomUser, TransactionHistory

admin.site.register(CustomUser)
admin.site.register(TransactionHistory)
