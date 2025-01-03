from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserPerference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{str(self.user)}'s perferences"
