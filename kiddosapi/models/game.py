from django.db import models

class Game(models.Model):
    
    name = models.CharField(max_length=50)
    kid = models.ForeignKey("Kid", related_name='games', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    min_age = models.IntegerField(null=True, blank=True)
    fave_games = models.ManyToManyField("Kid", through='FaveGame', related_name='fave_games')
    @property
    def faved(self):
        return self.__faved

    @faved.setter
    def faved(self, value):
        self.__faved = value