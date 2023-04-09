import six as six
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from user.models import User, UserRating, UserInterest, FreelancerInterest
from user.serializer import UserDataSerial, Rating, InterestDataSerializer, FreelancerSerializer
from user.utils import Util


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def activatepw(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        users = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        users = None
    if users is not None and account_activation_token.check_token(users, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        return Response({
            "message": "User Verified!",
            "user_id": uid,
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": "Invalid Activation Link!",
        },
            status=status.HTTP_400_BAD_REQUEST, )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        users = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        users = None
    if users is not None and account_activation_token.check_token(users, token):
        users.is_verified = True
        users.save()
        uid = force_str(urlsafe_base64_decode(uidb64))
        return Response({
            "message": "Email Verified!",
            "user_id": uid,
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": "Invalid Activation Link!",
        },
            status=status.HTTP_400_BAD_REQUEST, )


# Create your views here.


class Create_User(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data
        address = data['address']
        name = data['name']
        user_image = request.FILES.get('image', False)
        phone = request.data['phone']

        try:
            if data['name'] == '':
                name = None
            if data['address'] == '':
                address = None
            if data['phone'] == '':
                phone = None
            if request.FILES.get('image', False) is False:
                user_image = ''
            userSign = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                address=address,
                name=name,
                user_image=user_image,
                phone=int(phone),
            )
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('../templates/emailtemplate.html', {
                'user': userSign,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(userSign.pk)),
                'token': account_activation_token.make_token(userSign),
            })
            to_email = data['email']
            data = {'email_body': message,
                    'email': to_email, 'subject': mail_subject}
            Util.send_email(data)
            userSign.save()
            return Response({
                "message": "Verification link sent!",
            }, status=status.HTTP_200_OK)

        except:
            return Response({
                "message": "Error!",
            },
                status=status.HTTP_400_BAD_REQUEST, )


class Login_User(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            data = request.data
            username = data['username']
            password = data['password']
            try:
                user = authenticate(username=username, password=password)
                if user is not None:
                    refresh = RefreshToken.for_user(user)
                    login(request, user)
                    userdetails = User.objects.get(username__iexact=username)
                    usertype = userdetails.user_type
                    serializer = UserDataSerial(userdetails, many=False)
                    if not userdetails.is_verified:
                        reverify(request, userdetails, userdetails.email)
                    response = {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user_data": serializer.data,
                        "user_type": usertype,
                    }
                    return Response(response, status=status.HTTP_200_OK)

                else:
                    return Response({
                        "message": "Username or password doesn't match!",
                    }, status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                return Response(status=status.HTTP_204_NO_CONTENT)


class emailpass(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            emails = data['email']
            signupdata = User.objects.get(email=emails)
            current_site = get_current_site(request)
            mail_subject = 'Change Your Password.'
            message = render_to_string('../templates/passwordtemplate.html', {
                'user': signupdata,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(signupdata.pk)),
                'token': account_activation_token.make_token(signupdata),
            })
            to_email = emails
            data = {'email_body': message,
                    'email': to_email, 'subject': mail_subject}
            Util.send_email(data)
            messages.success(request, "")
            return Response({"message": "Check your email for password reset link", }, status=status.HTTP_200_OK, )
        except:
            return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)


def reverify(request, signupdata, emails):
    try:
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('../templates/emailtemplate.html', {
            'user': signupdata,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(signupdata.pk)),
            'token': account_activation_token.make_token(signupdata),
        })
        to_email = emails
        data = {'email_body': message,
                'email': to_email, 'subject': mail_subject}
        Util.send_email(data)
        return Response({"message": "Check your email for email verification link!", }, status=status.HTTP_200_OK, )
    except:
        return Response({
            "message": "Error!",
        },
            status=status.HTTP_400_BAD_REQUEST, )


class forgetpw(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            newpw = data['password']
            repw = data['repassword']
            if newpw == repw:
                userdata = User.objects.get(email=kwargs['email'])
                userdata.set_password(newpw)
                userdata.save()
                return Response({"message": "The password has been reset!", }, status=status.HTTP_200_OK, )
            else:
                return Response({"message": "Password does not match", }, status=status.HTTP_406_NOT_ACCEPTABLE, )
        except:
            return Response({
                "message": "Error!",
            },
                status=status.HTTP_400_BAD_REQUEST, )


class details(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            name = data['name']
            image = request.FILES.get('image')
            address = data['address']
            contact = data['phone']
            userData = User.objects.get(id=request.user.id)
            userData.name = name
            userData.user_image.delete()
            userData.user_image = image
            userData.phone = contact
            userData.address = address
            userData.save()
            return Response({"message": "The details has been updated!", }, status=status.HTTP_200_OK, )
        except:
            return Response({
                "message": "Error!",
            },
                status=status.HTTP_400_BAD_REQUEST, )

    def get(self, request, *args, **kwargs):
        userData = User.objects.get(id=request.user.id)
        serial = UserDataSerial(userData, many=False)
        return Response(serial.data, status=status.HTTP_200_OK)


class changepass(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            oldpass = data['oldpassword']
            newpw = data['password']
            repw = data['repassword']
            user = authenticate(username=request.user, password=oldpass)
            if user is not None:
                if newpw == repw:
                    userdata = User.objects.get(id=request.user.id)
                    userdata.set_password(newpw)
                    userdata.save()
                    return Response({"message": "The password has been updated!", }, status=status.HTTP_200_OK, )
                else:
                    return Response({
                        "message": "The password doesn't match",
                    },
                        status=status.HTTP_400_BAD_REQUEST, )
            else:
                return Response({
                    "message": "Wrong Password!",
                },
                    status=status.HTTP_400_BAD_REQUEST, )
        except:
            return Response({
                "message": "Error!",
            },
                status=status.HTTP_400_BAD_REQUEST, )


class ratingsAdd(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        receiver_id = data['receiver']
        rating = data['rating']
        UserRating(rating_giver_id=request.user.id, rating_receiver_id=receiver_id, rating=rating).save()
        return Response({"message": "The password has been updated!", }, status=status.HTTP_200_OK, )


class UserRatingData(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.query_params.get('id')
        detail = UserRating.objects.filter(rating_receiver_id=user)
        count = 0
        u = UserRating.objects.filter(rating_receiver_id=id).values('rating')
        a = UserRating.objects.filter(rating_receiver_id=id).all().distinct().count()
        for i in u:
            count += i
        r = int(count / a)
        ratings = Rating(detail, many=True)
        return Response({"overall_rating": r, "data": ratings}, status=status.HTTP_200_OK, )


class InterestData(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = UserInterest.objects.all()
        serializer = InterestDataSerializer(data, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK, )


class UserInterestData(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        itemlist = request.query_params.getlist('ids')
        data, _ = FreelancerInterest.objects.get_or_create(user=request.user.id)
        for i in itemlist:
            data.item.add(i)
            data.save()
        return Response({'data': 'Interest Added'}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        data = FreelancerInterest.objects.filter(user_id=request.user.id)
        serializer = FreelancerSerializer(data, many=False)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK, )
