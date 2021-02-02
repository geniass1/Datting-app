from django.db import models
from user.models import NewUser


class Likes(models.Model):
    who = models.OneToOneField(NewUser, on_delete=models.CASCADE, related_name='who_likes')
    whom = models.OneToOneField(NewUser, on_delete=models.CASCADE, related_name='whom_likes')
