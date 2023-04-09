from django.contrib import admin

# Register your models here.
from order.models import clientOrder, orderProgress

admin.site.register([clientOrder, orderProgress])
