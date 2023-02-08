from django.contrib import admin

# Register your models here.
from .models import Bill,Party,TrainInformation,Transaction

admin.site.register(Bill)
admin.site.register(TrainInformation)
admin.site.register(Transaction)
admin.site.register(Party)