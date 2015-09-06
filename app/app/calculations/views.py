#!/usr/bin/env python
# encoding: utf-8

from annoying.decorators import render_to, ajax_request

from .forms import PunchingForm
from .punching import compute_punching as cp
from .consts import *


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
        vrdc, vrdmax, vrdcs, errors, info = cp(**form.cleaned_data)
        if errors:
            result['success'] = False
            result['punching_errors'] = errors
        else:
            result['success'] = True
            result['info'] = info
            result['vrdc'] = round(vrdc / MPa, 3)
            result['vrdmax'] = round(vrdmax / MPa, 3)
            result['vrdcs'] = round(vrdcs / MPa, 3)
    else:
        result['success'] = False
        result['errors'] = form.errors
    return result
