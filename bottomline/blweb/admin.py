from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from blweb.models import VehicleModel, VehicleOption, VehicleMake, Profile, VehicleConfig


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(VehicleModel)
admin.site.register(VehicleMake)
admin.site.register(VehicleOption)
admin.site.register(VehicleConfig)

