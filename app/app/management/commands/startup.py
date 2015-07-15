#!/usr/bin/env python
# encoding: utf-8

from django.core.management.base import BaseCommand

import app.startup


class Command(BaseCommand):

    def handle(self, *args, **options):
        app.startup.run_startup()
