from django.contrib import admin
from .models import CustomUser, HouseOwner, Tenant


admin.site.register(CustomUser)
admin.site.register(HouseOwner)
admin.site.register(Tenant)

