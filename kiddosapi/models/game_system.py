from django.db import models


class GameSystem(models.Model):

    name = models.CharField(max_length=50)