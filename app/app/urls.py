#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += patterns('app.views',
    url(r'^$', 'home', name='home'),
)
