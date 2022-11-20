from rest_framework import serializers
from django.contrib.auth.models import User


class FirstRegistrationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()

    class Meta:
        model = User
        fields = ['phone', ]
