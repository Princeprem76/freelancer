from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from user.models import User, UserInterest


class clientOrder(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    order_name = models.CharField('OrderName', max_length=150, null=False)
    description = models.TextField('Description', null=False, blank=False)
    order_category = models.ManyToManyField(UserInterest, related_name='Order_Category')
    order_price = models.PositiveIntegerField('Price')
    image = models.ImageField(upload_to='order_image/', blank=True, null=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.order_name


class orderProgress(models.Model):
    order = models.ForeignKey(clientOrder, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE)

    class status(models.IntegerChoices):
        PENDING = 1, _('Pending')
        ONPROGRESS = 2, _('Onprogress')
        COMPLETED = 3, _('Completed')

    orderStatus = models.IntegerField(choices=status.choices, null=True, blank=True)
    applicants = models.ManyToManyField(User, related_name='Applicant')
