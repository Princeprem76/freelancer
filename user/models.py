from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .manager import UserManager


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('UserName', max_length=120, null=False, blank=False, unique=True)
    email = models.EmailField(_('Email Address'), unique=True)
    name = models.CharField('Name', max_length=150, null=True, blank=True)
    user_image = models.ImageField(upload_to='user_image/', blank=True, null=True)
    phone = models.PositiveBigIntegerField('Phone Number', unique=True, blank=True, null=True)
    address = models.CharField('Address', max_length=80, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class UserType(models.IntegerChoices):
        CLIENT = 1, _('Client')
        ADMIN = 2, _('Admin')
        FREELANCER = 3, _('Freelancer')

    user_type = models.IntegerField(choices=UserType.choices, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.user_type == self.UserType.ADMIN

    @property
    def is_client(self):
        "Is the user a client member?"
        return self.user_type == self.UserType.CLIENT

    @property
    def is_freelancer(self):
        "Is the user a freelancer member?"
        return self.user_type == self.UserType.FREELANCER

    def get_image(self):
        if not self.user_image:
            return '/media/user_image/user.jpg'
        else:
            return self.user_image


class UserRating(models.Model):
    rating_receiver = models.ForeignKey(User,related_name='Receiver', on_delete=models.CASCADE)
    rating_giver = models.ForeignKey(User,related_name='Giver', on_delete=models.CASCADE)
    rating = models.IntegerField('Rating', null=True, blank=True)
    review = models.TextField('Review', null=True, blank=True)


class UserInterest(models.Model):
    interests = models.CharField('Interest', max_length=150, blank=True, null=True)

    def __str__(self):
        return self.interests


class FreelancerInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interests = models.ManyToManyField(UserInterest, related_name='Interest')
