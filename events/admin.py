from django.contrib import admin

from .models import ViolationModel, ViolationImageModel, RecycleModel, RecycleImageModel, ChargingStationModel, \
    ChargingStationImageModel


@admin.register(ViolationModel)
class ViolationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'geocode', 'lat', 'long']


@admin.register(ViolationImageModel)
class ViolationImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'violation']


@admin.register(RecycleModel)
class RecycleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'geocode', 'lat', 'long', 'get_working_days_display', 'opening', 'closing']


@admin.register(RecycleImageModel)
class RecycleImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'recycle']


@admin.register(ChargingStationModel)
class ChargingStationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'get_payment_method_display', 'get_charging_type_display']


@admin.register(ChargingStationImageModel)
class ChargingStationImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'station']
