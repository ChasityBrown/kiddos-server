from django.db import models

class KidMeetUp(models.Model):
    
    kid = models.ForeignKey("Kid", on_delete=models.CASCADE)
    meet_up = models.ForeignKey("MeetUp", on_delete=models.CASCADE)