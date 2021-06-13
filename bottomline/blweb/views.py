from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from blweb import utils


def index(request):
    count_info = {}
    count_info['makes'] = utils.get_make_count()
    count_info['models'] = utils.get_model_count()

    context = {'count_info': count_info}
    return render(request, 'landing.html', context=context)


@login_required
def profile(request):
    return render(request, 'profile.html')
