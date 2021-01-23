from django.db import models
from django.contrib.auth.models import User


class Record(models.Model):
    date = models.DateTimeField(null=False)

    value = models.FloatField(null=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
