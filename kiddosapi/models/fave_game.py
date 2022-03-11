from django.db import models

class FaveGame(models.Model):
    
    kid = models.ForeignKey("Kid", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)