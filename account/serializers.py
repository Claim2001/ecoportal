from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ParseError

from .models import TokenModel, ProfileModel
from .utils import pass_generator


class RegistrationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=12, required=True)
    code = serializers.CharField(max_length=5, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def create(self, validated_data):

        return super(RegistrationSerializer, self).create(validated_data)

    class Meta:
        model = ProfileModel
        fields = ['dob', 'gender', 'avatar', 'phone', 'first_name', 'last_name', 'code']
