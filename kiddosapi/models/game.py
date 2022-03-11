from django.db import models

class Game(models.Model):
    
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    kid = models.ForeignKey("Kid", on_delete=models.CASCADE)
    approved = models.BooleanField(null=True)
    min_age = models.IntegerField(null=True, blank=True)