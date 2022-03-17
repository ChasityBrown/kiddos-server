from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):

    name = models.CharField(max_length=50)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    fave_rooms = models.ManyToManyField("Kid", through='FaveRoom', related_name='fave_rooms')
    @property
    def faved(self):
        return self.__faved

    @faved.setter
    def faved(self, value):
        self.__faved = value