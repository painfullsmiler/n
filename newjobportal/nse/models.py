from django.db import models

# Create your models here.
class NseSettings(models.Model):
    client = models.CharField(max_length=100,default=None)
    nse_list = models.CharField(max_length=100,default=None)
    path = models.CharField(max_length=100)
    sender_email = models.CharField(max_length=50)

    def __str__(self):
        return self.client