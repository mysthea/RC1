#!/usr/bin/env python
# encoding: utf-8

from django import forms

from .models import Punching


class PunchingForm(forms.ModelForm):

    class Meta:
        model = Punching
        exclude = ['vrdc', 'vrdmax']

