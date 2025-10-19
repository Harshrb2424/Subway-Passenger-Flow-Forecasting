from django.db import models

class TrafficPrediction(models.Model):
    stop_name = models.CharField(max_length=100)
    line = models.IntegerField()
    hour = models.IntegerField()
    day = models.IntegerField()
    enter_count = models.FloatField()
    leave_count = models.FloatField()

    def __str__(self):
        return f"{self.stop_name} - {self.hour}:{self.day}"
    class Meta:
        app_label = 'traffic'
