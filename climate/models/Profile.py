from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    | Extends django.contrib.auth.models.User with additional propertes
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='key to User')
    canUpload = models.BooleanField(default=False, help_text='is allowed to upload raw data')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    | If a User is created, a Profile is created
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    | If a User is saved, its Profile is saved
    """
    instance.profile.save()
