from django.db import models
from django.contrib.auth.models import User, Permission

class Kid(models.Model):
    user = models.OneToOneField(User, related_name="kid", on_delete=models.CASCADE)
    age = models.IntegerField()
    parent = models.ForeignKey(User, related_name="parent", on_delete=models.CASCADE)
    