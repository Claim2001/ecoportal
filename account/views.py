import random
import re

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response

from account.models import ProfileModel, TokenModel
from knox.models import AuthToken

from account.serializers import RegistrationSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login, authenticate

from account.utils import pass_generator


class LoginAPI():
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


def generate_code():
    code = random.randint(10000, 99999)
    while TokenModel.objects.filter(code=code).exists():
        code = random.randint(10000, 99999)
    return code


class SendSMSVIew(GenericAPIView):
    def post(self, request, *args, **kwargs):
        if 'phone' not in self.request.POST:
            return Response({"message": "No phone in data"}, status=status.HTTP_400_BAD_REQUEST)
        phone = self.request.POST.get('phone')
        if not re.match(r'^998\d{9}$', phone):
            return Response({'message': 'Wrong phone format'}, status=status.HTTP_400_BAD_REQUEST)
        TokenModel.objects.filter(phone=phone).delete()
        TokenModel.objects.create(code=generate_code(), phone=phone)
        # send sms
        return Response({"message": "Sms is sent"}, status=status.HTTP_201_CREATED)


# Register API
class CodeConfirmView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        if self.request.POST.keys() != {"code", "phone"}:
            return Response({"message": "No code or phone in sent data"}, status=status.HTTP_400_BAD_REQUEST)
        code = self.request.POST.get('code')
        phone = self.request.POST.get('phone')
        if not re.match(r'^998\d{9}$', phone):
            return Response({'message': 'Wrong phone format'}, status=status.HTTP_400_BAD_REQUEST)
        if TokenModel.objects.filter(code=code, phone=phone).exists():
            tm = get_object_or_404(TokenModel, code=code, phone=phone)
            if User.objects.filter(username=tm.phone).exists():
                um = get_object_or_404(User, username=tm.phone)
                authenticate(request=self.request, username=um.username, password=um.password)
                login(request, um)
                auth = super(CodeConfirmView, self).post(request, format=None)
                TokenModel.objects.filter(phone=phone).delete()
                return Response({"token": auth.data["token"], "expiry": auth.data["expiry"], "isRegistered": True},
                                status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"isRegistered": False}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Wrong code and/or phone"}, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        if self.request.POST.keys() != {"code", "phone", "first_name", "last_name"}:
            return Response({"message": "Wrong data sent"}, status=status.HTTP_400_BAD_REQUEST)
        phone = self.request.POST.get('phone')
        code = self.request.POST.get('code')
        fn = self.request.POST.get('first_name')
        ln = self.request.POST.get('last_name')
        if TokenModel.objects.filter(phone=phone, code=code).count() == 0:
            return Response({"message": "Wrong phone and/or code"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=phone).exists():
            return Response({"message": "User already created"}, status=status.HTTP_400_BAD_REQUEST)
        um = User.objects.create(username=phone, first_name=fn, last_name=ln)
        um.set_password(pass_generator())
        um.save()
        TokenModel.objects.filter(phone=phone).delete()
        authenticate(request=self.request, username=um.username, password=um.password)
        login(request, um)
        auth = super(RegistrationView, self).post(request, format=None)
        return Response(
            {"message": "User was successfully created", "token": auth.data["token"], "expiry": auth.data["expiry"],
             "isRegistered": True}, status=status.HTTP_201_CREATED)


class CheckAuth(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({"message": "OK"})
