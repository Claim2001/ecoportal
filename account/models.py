from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.base import BaseModel
from django.contrib.auth.models import User

GENDERS = (
    ('woman', _('Woman')),
    ('man', _('Man')),
)


class TokenModel(BaseModel, models.Model):
    code = models.CharField(max_length=5)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.code + ' ' + self.phone

    class Meta:
        verbose_name = 'token'
        verbose_name_plural = 'tokens'


class ProfileModel(BaseModel, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDERS)
    avatar = models.ImageField(upload_to='profiles', blank=True, null=True)

    def __str__(self):
        return self.user.username + ' | ' + self.user.get_full_name()

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
