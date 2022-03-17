from django.db import models

class FaveGame(models.Model):
    
    kid = models.ForeignKey("Kid", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.game.name} favorited by {self.kid}'  