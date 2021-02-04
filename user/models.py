from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

subscription_choices = (
    ("Standart", "Standart"),
    ("VIP", "VIP"),
    ("Premium", "Premium"),
)


class NewUser(AbstractUser):
    username = models.CharField('username', max_length=50, unique=True)
    email = models.EmailField('email', max_length=254, unique=True)
    password = models.CharField('password', max_length=50)
    subscription = models.CharField('sub', blank=True, max_length=250, choices=subscription_choices, default="Standart")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

