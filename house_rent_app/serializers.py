from rest_framework import serializers
from .models import Location
from accounts.models import Tenant, HouseOwner



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("name",)  
        




