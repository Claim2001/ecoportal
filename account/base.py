from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(editable=False, null=True, blank=True)
    updated_at = models.DateTimeField(editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        indexes = (
            BrinIndex(fields=('created_at', 'updated_at')),
        )
        abstract = True


class LocationModel(models.Model):
    lat = models.FloatField()
    long = models.FloatField()

    class Meta:
        abstract = True
