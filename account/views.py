import random
import re
import string

from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from account.models import ProfileModel, TokenModel

from account.serializers import FirstRegistrationSerializer


def generate_code():
    return random.randint(10000, 99999)


class FirstRegistrationView(CreateAPIView):
    serializer_class = FirstRegistrationSerializer

    def post(self, request, *args, **kwargs):
        phone = self.request.POST.get('phone')
        if not re.match(r'^998\d{9}$', phone):
            return Response({'message': 'Wrong phone format'}, status=status.HTTP_400_BAD_REQUEST)
        if ProfileModel.objects.filter(phone=phone).exists():
            pm = get_object_or_404(ProfileModel, phone=phone)
            um = get_object_or_404(User, profile=pm)
            if um.is_active:
                return Response({'message': 'User already created'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                TokenModel.objects.filter(user=um).delete()
                TokenModel.objects.create(user=um, code=generate_code())
                # send sms
                return Response({'message': 'Sms code was resent'}, status=status.HTTP_201_CREATED)
        else:
            um = User.objects.create(username=phone, is_active=False)
            um.set_password(phone)
            um.save()
            pm = ProfileModel.objects.create(user=um, phone=phone)
            TokenModel.objects.create(user=um, code=generate_code())
            # send sms
            return Response({'message': 'User was created successfully'}, status=status.HTTP_201_CREATED)


class LastRegistrationView(CreateAPIView):
    def post(self, request, *args, **kwargs):

        return super(LastRegistrationView, self).post(request)