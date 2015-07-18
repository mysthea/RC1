#!/usr/bin/env python
# encoding: utf-8

from annoying.decorators import render_to

from .forms import PunchingForm


@render_to('home.html')
def home(request):
    return {}


@render_to('punching.html')
def punching(request):
    form = PunchingForm(request.POST or None)
    return {'form': form}
