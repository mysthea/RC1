#!/usr/bin/env python
# encoding: utf-8

from django import forms

from .models import Punching

INITIAL_VALUE_CHOICE_DICT = {
    'c_class': 'C20/25',
    's_class': 'RB500',
    'dsw': '8',
    'support': 'słup wewnętrzny',
    'sect': 'prostokątny',
    'dsit': 'trwała',
}


class PunchingForm(forms.ModelForm):

    class Meta:
        model = Punching
        exclude = ['vrdc', 'vrdmax']

    def __init__(self, *args, **kwargs):
        super(PunchingForm, self).__init__(*args, **kwargs)

        for k, v in INITIAL_VALUE_CHOICE_DICT.items():
            field = self.fields.get(k)
            initial_index = next(
                [choice[0] for choice in field.choices
                 if choice[1] == v].__iter__(), None)
            if initial_index:
                self.initial[k] = str(initial_index)
