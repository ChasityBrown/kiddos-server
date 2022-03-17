from django.db import models

class FaveRoom(models.Model):
    
    kid = models.ForeignKey("Kid", on_delete=models.CASCADE)
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.room.name} favorited by {self.kid}'