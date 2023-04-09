from django.db import models

# Create your models here.
from order.models import clientOrder
from user.models import User


class Payment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(clientOrder, on_delete=models.CASCADE)
    transactionId = models.CharField('Transaction', null=True)
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    gateway = models.CharField('Payment_Method',max_length=120)

    def __str__(self):
        return self.client.username

