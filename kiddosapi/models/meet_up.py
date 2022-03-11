from django.db import models

class MeetUp(models.Model):
    
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    kid = models.ForeignKey("Kid", on_delete=models.CASCADE)
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    game_system = models.ForeignKey("GameSystem", on_delete=models.CASCADE)
    approved = models.BooleanField(null=True)
    attendees = models.ManyToManyField("Kid", through="KidMeetUp", related_name="attending")
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value