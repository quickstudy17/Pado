from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(null=True, blank=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)