from django.db import models
from account.base import BaseModel, LocationModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

TITLES = (
    ("1", _("Illegal Dump")),
    ("2", _("Deforestation")),
    ("3", _("Water Pollution")),
)

RECYCLE_TYPES = (
    ("1", _("Scrap metal")),
    ("2", _("Waste paper")),
    ("3", _("Glass")),
    ("4", _("Mechanism")),
    ("5", _("Furniture")),
    ("6", _("Plastic")),
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


# class RecycleModel(BaseModel, LocationModel, models.Model):
#     title = models.CharField(max_length=255)
#     recycle_types = models.CharField(max_length=30, choices=RECYCLE_TYPES)
#
#
# class RecycleImageModel(BaseModel, models.Model):
#     image = models.ImageField(upload_to='recycles')
#     recycle = models.ForeignKey(RecycleModel, on_delete=models.CASCADE)
