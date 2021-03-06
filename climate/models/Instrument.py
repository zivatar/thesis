import os
from django.db import models


def get_image_path_instrument1(instance, filename):
    """
    Defines absolute path of an uploaded image

    :param instance: Instrument object
    :param filename: original file name
    :return: '{BASE_PATH}/uploads/instrument/{site_id}'
    """
    return os.path.join('uploads', 'instrument', str(instance.siteId.pk))


class Instrument(models.Model):
    """
    | Instrument model
    | It has an autogenerated ID
    | Foreign key to Site objects
    | Unique: title
    """
    id = models.AutoField(primary_key=True, help_text='autogenerated id')
    siteId = models.ForeignKey('climate.Site', blank=True, null=True, help_text='foreign key for Site table')
    title = models.CharField(max_length=100, unique=True, help_text='unique title of the instrument')
    comment = models.TextField(blank=True, help_text='any additional information')
    type = models.CharField(max_length=50,
                            help_text='manufacturer and type of the instrument (e.g. LaCrosse WS-3600)')
    isActive = models.BooleanField(default=True, help_text='is active')
    primaryImage = models.ImageField(upload_to=get_image_path_instrument1, blank=True, null=True,
                                     help_text='representative image of the instrument')
