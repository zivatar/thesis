import os
from django.db import models


def get_image_path_instrument1(instance):
    return os.path.join('uploads', 'instrument', str(instance.siteId.pk))


class Instrument(models.Model):
    id = models.AutoField(primary_key=True)
    siteId = models.ForeignKey('climate.Site', blank=True, null=True)
    title = models.CharField(max_length=100, unique=True)
    comment = models.TextField(blank=True)
    type = models.CharField(max_length=50)
    isActive = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)
    primaryImage = models.ImageField(upload_to=get_image_path_instrument1, blank=True, null=True)
