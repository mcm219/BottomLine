from blweb.models import VehicleMake, VehicleModel


#
# This module contains a variety of helper functions that can be used from
# multiple places within the bottomline application.
#

# a helper function that returns the total number of vehicle makes
def get_make_count():
    return VehicleMake.objects.count()


# a helper function that returns the total number of vehicle models
def get_model_count():
    return VehicleModel.objects.count()
