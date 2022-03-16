from django.db import models

class Game(models.Model):
    
    name = models.CharField(max_length=50)
    kid = models.ForeignKey("Kid", related_name='games', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    min_age = models.IntegerField(null=True, blank=True)