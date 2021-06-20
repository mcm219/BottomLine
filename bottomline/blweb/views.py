from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from blweb import utils
from blweb.forms import ShopperSignupForm, DealerSignupForm


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
        form = ShopperSignupForm(request.POST)
    else:
        form = ShopperSignupForm()

    if form.is_valid():
        for name, value in form.cleaned_data.items():
            print("{}: ({}) {}".format(name, type(value), value))
        print("Account Type: {}".format(form.account_type))
        return render(request, 'signup_success.html')

    return render(request, 'account_signup.html', {"method": request.method, "form": form})


# use the dealer_signup.html template for account signups. This view is specifically for car dealers to
# create an account.
def dealer_signup(request):
    if request.method == "POST":
        form = DealerSignupForm(request.POST)
    else:
        form = DealerSignupForm()

    if form.is_valid():
        for name, value in form.cleaned_data.items():
            print("{}: ({}) {}".format(name, type(value), value))
        print("Account Type: {}".format(form.account_type))
        return render(request, 'signup_success.html')

    return render(request, 'dealer_signup.html', {"method": request.method, "form": form})



