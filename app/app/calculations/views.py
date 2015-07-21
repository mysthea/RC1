#!/usr/bin/env python
# encoding: utf-8

from annoying.decorators import render_to, ajax_request

from .forms import PunchingForm
from .punching import compute_punching as cp


@render_to('calculations/home.html')
def home(request):
    return {}


@render_to('calculations/punching.html')
def punching(request):
    form = PunchingForm(request.POST or None)
    return {'form': form}


# api views

@ajax_request
def compute_punching(request):
    result = {}
    form = PunchingForm(request.POST or None)
    if form.is_valid():
        # form.save()
        vrdc, vrdmax, errors = cp(**form.cleaned_data)
        if errors:
            result['success'] = False
            result['punching_errors'] = errors
        else:
            result['success'] = True
            result['vrdc'] = vrdc
            result['vrdmax'] = vrdmax
    else:
        result['success'] = False
        result['errors'] = form.errors
    return result
