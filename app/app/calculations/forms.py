#!/usr/bin/env python
# encoding: utf-8

from django import forms

from .models import Punching

INITIAL_VALUE_CHOICE_DICT = {
    'c_class': 'C20/25',
    's_class': 'BSt500',
    'dsw': '8',
    'support': 'słup wewnętrzny',
    'sect': 'prostokątny',
    'dsit': 'trwała',
}

INITIAL_VALUE_INPUT_DICT = {
    'b': 40.0,
    'h': 30.0,
    'dx': 21.0,
    'dy': 22.5,
    'lx': 0.0,
    'ly': 0.0,
    'ad': 0.0,
    'lambda_u': 0,
    'asx': 11.3,
    'asy': 11.3,
    'ved': 350.0,
    'beta': 1.15,
}

ATTRS_DECIMAL_DICT = {
    'b': (15.0, 150.0, 1.0),
    'h': (15.0, 150.0, 1.0),
    'dx': (15.0, 50.0, 0.5),
    'dy': (15.0, 50.0, 0.5),
    'lx': (0.0, 250.0, 5.0),
    'ly': (0.0, 250.0, 5.0),
    'ad': (0.0, 20.0, 1.0), # TODO: try to change into min(dx, dy)
    'asx': (0.0, 50.0, 0.1),
    'asy': (0.0, 50.0, 0.1),
    'ved': (0.0, 5000.0, 1.0),
    'beta': (1.00, 2.50, 0.01),
}


class PunchingForm(forms.ModelForm):

    class Meta:
        model = Punching
        exclude = ['vrdc', 'vrdmax']

    def __init__(self, *args, **kwargs):
        super(PunchingForm, self).__init__(*args, **kwargs)

        for k, v in INITIAL_VALUE_CHOICE_DICT.items():
            field = self.fields.get(k)
            field.empty_label = None
            initial_index = next(
                [choice[0] for choice in field.choices
                 if choice[1] == v].__iter__(), None)
            if initial_index:
                self.initial[k] = str(initial_index)
                self.widget = forms.DecimalField()

        for k, v in INITIAL_VALUE_INPUT_DICT.items():
            self.initial[k] = v

        for k, v in ATTRS_DECIMAL_DICT.items():
            self.fields[k].widget.attrs.update({
                'min': v[0],
                'max': v[1],
                'step': v[2],
            })

        self.fields['lambda_u'].widget.attrs.update(
            {'min': 0, 'max': 100, 'step': 5})
