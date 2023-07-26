from django.contrib import admin
from .models import Location, Picture, ListingAlbum, Listing

admin.site.register(Location)
admin.site.register(Picture)
admin.site.register(ListingAlbum)
admin.site.register(Listing)