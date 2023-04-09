from django.contrib import admin

# Register your models here.
from user.models import User, UserInterest, UserRating, FreelancerInterest

admin.site.register([User, UserInterest, UserRating, FreelancerInterest])
