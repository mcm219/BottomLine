from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from blweb import utils
from blweb.forms import SignupForm, VehicleConfigForm, VehicleMakeForm, VehicleModelForm, VehicleOptionsForm, \
    VehicleColorOptionsForm
from blweb.models import AccountType, VehicleConfig, VehicleOption, VehicleColor


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
            print("Vehicle Make: ", make.name)

            # We've started a new VehicleConfig
            veh_config = VehicleConfig.objects.create(make=make)

            # now save it in the session so it can be retrieved in other views later
            request.session['vehicle_config'] = veh_config.pk

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
        # handle the case where the session key is not set. redirect back to the main config page
        return HttpResponseRedirect('/vehicle_config')

    if request.method == "POST":
        model_form = VehicleModelForm(request.POST, prefix='mod', chosen_make=make)

        if model_form.is_valid():
            try:
                # retrieve our VehicleConfig primary key from the session
                veh_config_id = request.session.get('vehicle_config', None)
            except KeyError:
                # handle the case where the session key is not set. redirect back to the main config page
                return HttpResponseRedirect('/vehicle_config')

            if veh_config_id is not None:
                # get the actual object from the key
                veh_config = VehicleConfig.objects.get(pk=veh_config_id)

                # get the model
                model = model_form.cleaned_data.get('name')
                print("Vehicle Model: ", model)

                # add the model to the VehicleConfig
                veh_config.model = model
                veh_config.save()
            else:
                return HttpResponseRedirect('/vehicle_config')

            # send the user to the options page to add vehicle options
            return HttpResponseRedirect('/vehicle_config_options')
        else:
            context = {'model_form': model_form}
    else:
        context = {'model_form': VehicleModelForm(prefix='mod', chosen_make=make)}

    return render(request, 'vehicle_config_model.html', context)


# take the dict context and the VehicleConfig veh_config and add the options with pricing
# to the context (as a dictionary)
def add_option_price_context_dict(context, veh_config):
    if veh_config is None:
        return context

    context['veh_options'] = {}

    for option in VehicleOption.objects.filter(model=veh_config.model.pk).exclude(vehiclecolor__isnull=False):
        context['veh_options'][option.pk] = option.price

    return context


# take the dict context and the VehicleConfig veh_config and add the options with pricing
# to the context (as a dictionary)
def add_color_option_price_context_dict(context, veh_config):
    if veh_config is None:
        return context

    context['veh_color_options'] = {}

    for color in VehicleColor.objects.filter(model=veh_config.model.pk):
        context['veh_color_options'][color.pk] = color.price

    return context


def vehicle_config_options(request):
    try:
        veh_config_id = request.session.get("vehicle_config", None)
    except KeyError:
        # handle the case where the session key is not set. redirect back to the main config page
        return HttpResponseRedirect('/vehicle_config')

    if veh_config_id is not None:
        veh_config = VehicleConfig.objects.get(pk=veh_config_id)
        print("Options Page::Make: ", veh_config.make)
        print("Options Page::Model: ", veh_config.model)

    if request.method == "POST":
        options_form = VehicleOptionsForm(request.POST, prefix='options', chosen_model=veh_config.model.pk)
        colors_form = VehicleColorOptionsForm(request.POST, prefix='colors', chosen_model=veh_config.model.pk)
        context = {'options_form': options_form, 'colors_form': colors_form}

        if options_form.is_valid() and colors_form.is_valid():
            if veh_config_id is not None:
                # get the actual object from the key
                veh_config = VehicleConfig.objects.get(pk=veh_config_id)

                # get the options from the form
                options = options_form.cleaned_data.get('options')

                # get the color from the form
                color = colors_form.cleaned_data.get('colors')

                # add to the current vehicle config object
                veh_config.options.add(*options)
                veh_config.color = color
                veh_config.save()
            else:
                return HttpResponseRedirect('/vehicle_config')

            # send the user to the completion page to add vehicle options
            return HttpResponseRedirect('/vehicle_config_complete')
        else:
            context = {'options_form': options_form,
                       'colors_form': colors_form,
                       'veh_make': veh_config.make.name,
                       'veh_model': veh_config.model.name,
                       'veh_model_price': veh_config.model.price}

            context = add_option_price_context_dict(context=context,
                                                    veh_config=veh_config)
            context = add_color_option_price_context_dict(context=context,
                                                          veh_config=veh_config)
    else:
        context = {'options_form': VehicleOptionsForm(prefix='options', chosen_model=veh_config.model.pk),
                   'colors_form': VehicleColorOptionsForm(prefix='colors', chosen_model=veh_config.model.pk),
                   'veh_make': veh_config.make.name,
                   'veh_model': veh_config.model.name,
                   'veh_model_price': veh_config.model.price}

        context = add_option_price_context_dict(context=context,
                                                veh_config=veh_config)
        context = add_color_option_price_context_dict(context=context,
                                                      veh_config=veh_config)

    return render(request, 'vehicle_config_options.html', context)


def vehicle_config_complete(request):
    try:
        veh_config_id = request.session.get("vehicle_config", None)
    except KeyError:
        # handle the case where the session key is not set. redirect back to the main config page
        return HttpResponseRedirect('/vehicle_config')

    if veh_config_id is not None:
        # get the actual object from the key
        veh_config = VehicleConfig.objects.get(pk=veh_config_id)

        context = {'make': veh_config.make.name,
                   'model': veh_config.model.name,
                   'color': veh_config.color.name,
                   'options': veh_config.options}
    else:
        context = {}
    return render(request, 'vehicle_config_complete.html', context)
