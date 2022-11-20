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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    code = models.CharField(max_length=5)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ' | ' + self.code

    class Meta:
        verbose_name = 'token'
        verbose_name_plural = 'tokens'


class ProfileModel(BaseModel, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDERS)
    avatar = models.ImageField(upload_to='profiles', blank=True, null=True)
    phone = models.CharField(max_length=40, null=True, blank=True, unique=True)

    def __str__(self):
        return self.user.username + ' | ' + self.user.get_full_name()

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
