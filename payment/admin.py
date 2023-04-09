from django.contrib import admin

# Register your models here.
from payment.models import Payment

admin.site.register(Payment)
