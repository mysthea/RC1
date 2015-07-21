#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += patterns('app.calculations.views',
    url(r'^$', 'home', name='home'),
    url(r'^przebicie$', 'punching', name='punching'),

    # api
    url(r'^api/compute_punching$', 'compute_punching',
        name='compute_punching'),
)
