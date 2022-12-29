from django.db import models
from multiselectfield import MultiSelectField

from account.base import BaseModel, LocationModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

TITLES = (
    ("1", _("Illegal Dump")),
    ("2", _("Deforestation")),
    ("3", _("Water Pollution")),
)

RECYCLE_TYPES = (
    (1, _("Scrap metal")),
    (2, _("Waste paper")),
    (3, _("Glass")),
    (4, _("Mechanism")),
    (5, _("Furniture")),
    (6, _("Plastic")),
)

WORKING_DAYS = (
    (1, _("Monday")),
    (2, _("Tuesday")),
    (3, _("Wednesday")),
    (4, _("Thursday")),
    (5, _("Friday")),
    (6, _("Saturday")),
    (7, _("Sunday")),
)

PAYMENT_METHODS = (
    (1, _("Plastic card")),
    (2, _("Cash")),
    (3, _("App")),
)

CHARGING_TYPES = (
    (1, _("Slow")),
    (1, _("Fast")),
    (1, _("Rapid")),
    (1, _("Extra Fast")),
)


class ViolationModel(BaseModel, LocationModel, models.Model):
    title = models.CharField(choices=TITLES, max_length=20)
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.geocode + ' - ' + self.get_title_display()


class ViolationImageModel(BaseModel, models.Model):
    image = models.ImageField(upload_to='violations')
    violation = models.ForeignKey(ViolationModel, on_delete=models.CASCADE, related_name='image')


class RecycleModel(BaseModel, LocationModel, models.Model):
    name = models.CharField(max_length=255)
    recycle_types = MultiSelectField(choices=RECYCLE_TYPES, max_choices=6, max_length=20)
    working_days = MultiSelectField(choices=WORKING_DAYS, max_choices=7, max_length=20)
    opening = models.TimeField()
    closing = models.TimeField()
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' - ' + self.geocode


class RecycleImageModel(BaseModel, models.Model):
    image = models.ImageField(upload_to='recycles')
    recycle = models.ForeignKey(RecycleModel, on_delete=models.CASCADE, related_name='image')


class ChargingStationModel(BaseModel, LocationModel, models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    payment_method = MultiSelectField(choices=PAYMENT_METHODS, max_choices=3, max_length=20)
    charging_type = models.CharField(choices=CHARGING_TYPES, max_length=20)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + self.geocode


class ChargingStationImageModel(BaseModel, models.Model):
    image = models.ImageField(upload_to='charging stations')
    station = models.ForeignKey(ChargingStationModel, on_delete=models.CASCADE, related_name='image')
