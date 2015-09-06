#!/usr/bin/env python
# encoding: utf-8

"""
Code run at startup.
"""

from __future__ import absolute_import, division

from .models import Concrete, Steel, Diametersw, Support, Section, DesignSituation
from .consts import c_tab, s_tab, diameter_sw, supports, sections, design_situations


def run_startup():
    # create concretes
    for c_class in c_tab:
        Concrete.objects.get_or_create(type=c_class)

    # create steels
    for s_class in s_tab:
        Steel.objects.get_or_create(type=s_class)

    # create diameters in mm
    for dsw in diameter_sw:
        Diametersw.objects.get_or_create(value=dsw)

    for support in supports:
        Support.objects.get_or_create(type=support)
   
    for section in sections:
        Section.objects.get_or_create(type=section)

    # create design situations
    for design_situation in design_situations:
        DesignSituation.objects.get_or_create(type=design_situation)
