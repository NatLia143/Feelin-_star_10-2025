from django.db import models


class Instrument(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=10, blank=True) 

    def __str__(self):
        return f"{self.icon} {self.name}"
    


