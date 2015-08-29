#!/usr/bin/env python
# encoding: utf-8

"""
Code run at startup.
"""

from __future__ import absolute_import, division

from .models import Concrete, Steel, Diametersw, Support, Section, DesignSit


def run_startup():

    # create concretes
    c_classes = ['C12/15', 'C16/20', 'C20/25', 'C25/30', 'C30/37', 'C35/45',
                 'C40/50', 'C45/55', 'C50/60', 'C55/67', 'C60/75', 'C70/85',
                 'C80/95', 'C90/105']
    for c_class in c_classes:
        Concrete.objects.get_or_create(type=c_class)

    # create steels
    s_classes = ['RB400', 'RB400W', '35G2Y', '34GS', 'BSt420', '20G2VY-b',
                 'RB500', 'RB500W', 'B500SP', 'BSt500']
    for s_class in s_classes:
        Steel.objects.get_or_create(type=s_class)

    # create diameters in mm
    diameter_sw = [6, 8, 10, 12]
    for dsw in diameter_sw:
        Diametersw.objects.get_or_create(value=dsw)

    # create supports
    supports = ['słup wewnętrzny', 'słup krawędziowy X', 'słup krawędziowy Y', 'słup narożny',
                'ściana-naroże', 'ściana-koniec']
    for support in supports:
        Support.objects.get_or_create(type=support)

    # create sects
    sects = ['prostokątny', 'kołowy']
    for section in sects:
        Section.objects.get_or_create(type=sect)

    # create dsits
    dsits = ['trwała', 'przejściowa', 'wyjątkowa']
    for design_sit in dsits:
        DesignSit.objects.get_or_create(type=dsit)
