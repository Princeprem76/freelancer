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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from order.views import Orders, OrderApply, ApplicationDetails, AssignApplication, ChangeStatus, SearchOrder, AllOrder, \
    MyOrder, UploadFile
from payment.views import Order_payment
from user.views import Login_User, Create_User, forgetpw, activatepw, activate, details, changepass, InterestData, \
    UserInterestData, ratingsAdd, UserRatingData, emailpass, InterestSearch, SpecificUserData

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
    path('api/v1/usersearch/', InterestSearch.as_view(), name="User Interest Search"),
    path('api/v1/userdata/<int:id>/', SpecificUserData.as_view(), name="Specific User Data"),
    path('api/v1/apply/<int:id>/', OrderApply.as_view(), name="Apply for Order"),
    path('api/v1/applicants/<int:id>/', ApplicationDetails.as_view(), name="Application Details"),
    path('api/v1/assign/<int:id>/', AssignApplication.as_view(), name="Assign Applicants"),
    path('api/v1/completed/<int:id>/', ChangeStatus.as_view(), name="Order Completed"),
    path('api/v1/searchorder/', SearchOrder.as_view(), name="Search order"),
    path('api/v1/allorder/', AllOrder.as_view(), name="All order"),
    path('api/v1/myorder/', MyOrder.as_view(), name="freelancer assigned order"),
    path('api/v1/uploadfile/<int:id>/', UploadFile.as_view(), name="Order File Upload"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)