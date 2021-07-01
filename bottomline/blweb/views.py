from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from blweb import utils
from blweb.forms import SignupForm, VehicleConfigForm, VehicleMakeForm, VehicleModelForm
from blweb.models import AccountType


# This is the view for the BottomLine main landing page. It renders the landing.html template
# along with providing some relevant data


def index(request):
    count_info = {}
    count_info['makes'] = utils.get_make_count()
    count_info['models'] = utils.get_model_count()

    context = {'count_info': count_info}
    return render(request, 'landing.html', context=context)


@login_required
def profile(request):
    return render(request, 'profile.html')


# use the account_signup.html template for account signups. This view is specifically for car shoppers to
# create an account.
def account_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
    else:
        form = SignupForm()

    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.account_type = AccountType.SHOPPER.value
        user.save()

        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        login(request, user)

        return render(request, 'signup_success.html')

    return render(request, 'account_signup.html', {"method": request.method, "form": form})


# use the dealer_signup.html template for account signups. This view is specifically for car dealers to
# create an account.
def dealer_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
    else:
        form = SignupForm()

    if form.is_valid():
        user = form.save()
        user_profile = user.profile
        user.refresh_from_db()
        user_profile.account_type = AccountType.DEALER.value
        user.save()
        user_profile.save()

        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        login(request, user)

        return render(request, 'signup_success.html')

    return render(request, 'dealer_signup.html', {"method": request.method, "form": form})


# def vehicle_config(request):
#     if request.method == "POST":
#         #form = VehicleConfigForm(request.POST)
#         form = VehicleMakeForm(request.POST)
#         if form.is_valid():
#             pass
#             # get the make
#             make = form.cleaned_data.get('name')
#
#             # now create a new form for the VehicleModel
#             form = VehicleModelForm()
#     else:
#         form = VehicleMakeForm()
#
#     return render(request, 'vehicle_config.html', {"method": request.method, "form": form})

def vehicle_config(request):
    if request.method == "POST":
        make_form = VehicleMakeForm(request.POST)
        model_form = VehicleModelForm(request.POST)

        if make_form.is_valid() and model_form.is_valid():
            # Get the make
            make = make_form.cleaned_data.get('name')

            # See if a model was selected
            model = None


            # both make and model have been specified, this is a success
            # redirect to the next page for vehicle options
            return HttpResponseRedirect('/vehicle_options')
        elif make_form.is_valid() and not model_form.is_valid():
            # user has selected a make and clicked 'next'
            context = {'make_form': make_form, 'model_form': model_form}
        else:
            context = {'make_form': make_form}
    else:
        context = {
            'make_form': VehicleMakeForm(),
        }

    return render(request, 'vehicle_config.html', context)

