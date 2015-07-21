#!/usr/bin/env python
# encoding: utf-8

from django.core.management.base import BaseCommand

from app.calculations import startup


class Command(BaseCommand):

    def handle(self, *args, **options):
        startup.run_startup()
