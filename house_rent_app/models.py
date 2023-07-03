from django.db import models
from accounts.models import HouseOwner

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Listing(models.Model):
    house_owner = models.ForeignKey(HouseOwner, on_delete=models.SET_NULL, null=True)
    house_pictures = models.ImageField(upload_to= "house/owner", default="avatar.svg")
    house_description = models.TextField()
    location =  models.ForeignKey('Location',on_delete=models.SET_NULL, null=True)
    