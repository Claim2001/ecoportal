from django.contrib import admin

from .models import ViolationModel, ViolationImageModel


@admin.register(ViolationModel)
class ViolationAdmin(admin.ModelAdmin):
    list_display = ['title', 'lat', 'long']


@admin.register(ViolationImageModel)
class ViolationImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'violation']
