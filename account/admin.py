from django.contrib import admin

from account.models import TokenModel, ProfileModel


@admin.register(TokenModel)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['code', ]


@admin.register(ProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dob', 'gender']
