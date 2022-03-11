from django.db import models


class Room(models.Model):

    name = models.CharField(max_length=50)
    parent = models.ForeignKey("User", on_delete=models.CASCADE)