import random
import re
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView, CreateAPIView
from account.models import TokenModel, ProfileModel
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login, authenticate
from account.serializers import RegistrationSerializer, SMSSerializer, CodeConfirmSerializer
from account.utils import pass_generator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response


def generate_code():
    code = random.randint(10000, 99999)
    while TokenModel.objects.filter(code=code).exists():
        code = random.randint(10000, 99999)
    return code


class SendSMSView(GenericAPIView):
    @swagger_auto_schema(request_body=SMSSerializer,
                         responses={201: openapi.Response(description="Sent successfully"),
                                    400: openapi.Response(description="Wrong phone format")})
    def post(self, request, *args, **kwargs):
        """
        Send SMS API
            Body: {"phone": "998901234567"}
            Responses:  400 - {"message": "Wrong phone format"}
                        201 - {"message": "Sms is sent"}
        """
        serializer = SMSSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.data['phone']
        if not re.match(r'^998\d{9}$', phone):
            return Response({"message": "Wrong phone format"}, status=status.HTTP_400_BAD_REQUEST)
        TokenModel.objects.filter(phone=phone).delete()
        TokenModel.objects.create(code=generate_code(), phone=phone)
        # send sms
        return Response({"message": "Sms is sent"}, status=status.HTTP_201_CREATED)


# Register API
class CodeConfirmView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=CodeConfirmSerializer,
                         responses={201: openapi.Response(description="Sent successfully"),
                                    400: openapi.Response(description="Wrong phone format")})
    def post(self, request, *args, **kwargs):
        """
        Code Confirm API
                Body: {"phone": "998901234567", "code": "12345"}
                Responses: 400 - {"message": "Wrong phone format"}
                          202 - {"token": some_token, "expiry": some_date, "isRegistered": True}
                          100 - {"isRegistered": False}
                          400 - {"message": "Wrong code and/or phone"}
        """
        serializer = CodeConfirmSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        code = data['code']
        phone = data['phone']
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
                return Response({"isRegistered": False}, status=status.HTTP_100_CONTINUE)
        else:
            return Response({"message": "Wrong code and/or phone"}, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        phone = data['phone']
        code = data['code']
        fn = data['first_name']
        ln = data['last_name']
        avatar = data['avatar']
        role = data['role']
        if TokenModel.objects.filter(phone=phone, code=code).count() == 0:
            return Response({"message": "Wrong phone and/or code"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=phone).exists():
            return Response({"message": "User already created"}, status=status.HTTP_400_BAD_REQUEST)
        um = User.objects.create(username=phone, first_name=fn, last_name=ln)
        um.set_password(pass_generator())
        um.save()
        ProfileModel.objects.create(avatar=avatar, user=um, role=role)
        TokenModel.objects.filter(phone=phone).delete()
        authenticate(request=self.request, username=um.username, password=um.password)
        login(request, um)
        auth = super(RegistrationView, self).post(request, format=None)
        return Response(
            {"message": "User was successfully created", "token": auth.data["token"], "expiry": auth.data["expiry"],
             "isRegistered": True}, status=status.HTTP_201_CREATED)
