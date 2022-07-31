from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=140, null=True, blank=True)
    role = models.CharField(max_length=140)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance, role='new_user')
