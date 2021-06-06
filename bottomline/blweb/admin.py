from django.contrib import admin

from blweb.models import VehicleModel, VehicleOption, VehicleMake

admin.site.register(VehicleModel)
admin.site.register(VehicleMake)
admin.site.register(VehicleOption)

