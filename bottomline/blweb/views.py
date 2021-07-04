from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from blweb import utils
from blweb.forms import SignupForm, VehicleConfigForm, VehicleMakeForm, VehicleModelForm, VehicleOptionsForm
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


def vehicle_config(request):
    if request.method == "POST":
        make_form = VehicleMakeForm(request.POST, prefix='make')

        if make_form.is_valid():
            # Get the make
            make = make_form.cleaned_data.get('name')
            print("Vehicle Make: ", make)

            # both make and model have been specified, this is a success
            # redirect to the next page for vehicle options
            response = HttpResponseRedirect('/vehicle_config_model')
            response.set_cookie('VehicleMake', make)
            return response

        else:
            context = {'make_form': make_form}
    else:
        context = {
            'make_form': VehicleMakeForm(prefix='make'),
        }

    return render(request, 'vehicle_config_make.html', context)


def vehicle_config_model(request):
    try:
        # get the make from the cookie set earlier
        make = request.COOKIES['VehicleMake']
    except KeyError:
        # handle the case where the cookie is not set. redirect back to the main config page
        return HttpResponseRedirect('/vehicle_config')

    if request.method == "POST":

        model_form = VehicleModelForm(request.POST, prefix='mod', chosen_make=make)

        if model_form.is_valid():
            # get the model
            model = model_form.cleaned_data.get('name')
            print("Vehicle Model: ", model)

            return HttpResponseRedirect('/vehicle_config_options')
        else:
            context = {'model_form': model_form}
    else:
        context = {'model_form': VehicleModelForm(prefix='mod', chosen_make=make)}

    return render(request, 'vehicle_config_model.html', context)


def vehicle_config_options(request):
    if request.method == "POST":
        options_form = VehicleOptionsForm(request.POST, prefix='options')
    else:
        context = {'options_form': VehicleOptionsForm(prefix='options')}

    return render(request, 'vehicle_config_options.html', context)
