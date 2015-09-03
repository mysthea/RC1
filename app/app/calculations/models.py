#!/usr/bin/env python
# encoding: utf-8

from django.db import models


class Concrete(models.Model):
    # beton
    type = models.CharField(max_length=20, verbose_name='klasa')

    def __str__(self):
        return self.type


class Steel(models.Model):
    # stal
    type = models.CharField(max_length=20, verbose_name='klasa')

    def __str__(self):
        return self.type


class Diametersw(models.Model):
    # średnica in mm
    value = models.IntegerField(verbose_name='wartość')

    def __str__(self):
        return str(self.value)


class Support(models.Model):
    # podpora
    type = models.CharField(max_length=30, verbose_name='typ')

    def __str__(self):
        return self.type


class Section(models.Model):
    # przekrój
    type = models.CharField(max_length=20, verbose_name='typ')

    def __str__(self):
        return self.type


class DesignSituation(models.Model):
    # sytuacja obliczeniowa
    type = models.CharField(max_length=20, verbose_name='typ')

    def __str__(self):
        return self.type


class Punching(models.Model):
    # materials
    c_class = models.ForeignKey(Concrete)
    s_class = models.ForeignKey(Steel)
    dsw = models.ForeignKey(Diametersw)

    # geometry
    support = models.ForeignKey(Support)
    section = models.ForeignKey(Section)
    b = models.DecimalField(max_digits=4, decimal_places=1)
    h = models.DecimalField(max_digits=4, decimal_places=1)
    dx = models.DecimalField(max_digits=4, decimal_places=1)
    dy = models.DecimalField(max_digits=4, decimal_places=1)
    lx = models.DecimalField(max_digits=4, decimal_places=1)
    ly = models.DecimalField(max_digits=4, decimal_places=1)
    ad = models.DecimalField(max_digits=3, decimal_places=1)
    lambda_u = models.IntegerField()
    asx = models.DecimalField(max_digits=3, decimal_places=1)
    asy = models.DecimalField(max_digits=3, decimal_places=1)

    # work conditions
    design_situation = models.ForeignKey(DesignSituation)
    ved = models.DecimalField(max_digits=5, decimal_places=1)
    beta = models.DecimalField(max_digits=3, decimal_places=2)

    #results
    vrdc = models.DecimalField(
        max_digits=5, decimal_places=3, null=True, blank=True)
    vrdmax = models.DecimalField(
        max_digits=5, decimal_places=3, null=True, blank=True)
