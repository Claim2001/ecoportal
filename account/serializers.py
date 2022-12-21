from rest_framework import serializers
from .models import ProfileModel, ROLES


class SMSSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)


class CodeConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)


class RegistrationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=12, required=True)
    code = serializers.CharField(max_length=5, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    avatar = serializers.ImageField(required=True)
    role = serializers.ChoiceField(choices=ROLES, required=True)

    class Meta:
        model = ProfileModel
        fields = ['avatar', 'phone', 'first_name', 'last_name', 'code', 'role']
