from django.db import models
from django.contrib.auth.models import User

class Kid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    parent = models.ForeignKey(User, related_name="parent", on_delete=models.CASCADE)