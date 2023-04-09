"""
URL configuration for freelancing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from order.views import Orders
from payment.views import Order_payment
from user.views import Login_User, Create_User, forgetpw, activatepw, activate, details, changepass, InterestData, \
    UserInterestData, ratingsAdd, UserRatingData, emailpass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', Login_User.as_view(), name="login"),
    path('api/v1/register/', Create_User.as_view(), name="register"),
    path('api/v1/activate/', activate.as_view(), name='activate'),
    path('api/v1/activatepw/', activatepw.as_view(), name='password reset'),
    path('api/v1/emailpw/', emailpass.as_view(), name="Email recovery"),
    path('api/v1/userdetails/', details.as_view(), name="user details"),
    path('api/v1/changepassword/', changepass.as_view(), name="change password"),
    path('api/v1/forgetpassword/', forgetpw.as_view(), name="forget password"),
    path('api/v1/interestdata/', InterestData.as_view(), name="Interest"),
    path('api/v1/userinterest/', UserInterestData.as_view(), name="UserInterest"),
    path('api/v1/payments/', Order_payment.as_view(), name="Payment"),
    path('api/v1/addrating/', ratingsAdd.as_view(), name="Give Rating"),
    path('api/v1/userrating/<int:id>/', UserRatingData.as_view(), name="User Rating"),
    path('api/v1/orders/', Orders.as_view(), name="Client Order"),

]
