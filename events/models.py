from django.db import models
from account.base import BaseModel, LocationModel
from django.utils.translation import gettext_lazy as _

TITLES = (
    ("1", _("Illegal Dump")),
    ("2", _("Deforestation")),
    ("3", _("Water Pollution")),
)


class ViolationModel(BaseModel, LocationModel, models.Model):
    title = models.CharField(choices=TITLES, max_length=20)
    comment = models.TextField()


class ViolationImageModel(BaseModel, models.Model):
    image = models.ImageField(upload_to='violations')
    violation = models.ForeignKey(ViolationModel, on_delete=models.CASCADE)
