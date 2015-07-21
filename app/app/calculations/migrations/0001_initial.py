# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concrete',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(verbose_name='klasa', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DesignSit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(verbose_name='typ', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Diametersw',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('value', models.IntegerField(verbose_name='wartość')),
            ],
        ),
        migrations.CreateModel(
            name='Punching',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('b', models.DecimalField(decimal_places=1, max_digits=4)),
                ('h', models.DecimalField(decimal_places=1, max_digits=4)),
                ('dx', models.DecimalField(decimal_places=1, max_digits=4)),
                ('dy', models.DecimalField(decimal_places=1, max_digits=4)),
                ('lx', models.DecimalField(decimal_places=1, max_digits=4)),
                ('ly', models.DecimalField(decimal_places=1, max_digits=4)),
                ('ad', models.DecimalField(decimal_places=1, max_digits=3)),
                ('lambda_u', models.IntegerField()),
                ('asx', models.DecimalField(decimal_places=1, max_digits=3)),
                ('asy', models.DecimalField(decimal_places=1, max_digits=3)),
                ('ved', models.DecimalField(decimal_places=1, max_digits=5)),
                ('beta', models.DecimalField(decimal_places=2, max_digits=3)),
                ('vrdc', models.DecimalField(blank=True, null=True, decimal_places=3, max_digits=5)),
                ('vrdmax', models.DecimalField(blank=True, null=True, decimal_places=3, max_digits=5)),
                ('c_class', models.ForeignKey(to='calculations.Concrete')),
                ('dsit', models.ForeignKey(to='calculations.DesignSit')),
                ('dsw', models.ForeignKey(to='calculations.Diametersw')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(verbose_name='typ', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Steel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(verbose_name='klasa', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(verbose_name='typ', max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='punching',
            name='s_class',
            field=models.ForeignKey(to='calculations.Steel'),
        ),
        migrations.AddField(
            model_name='punching',
            name='sect',
            field=models.ForeignKey(to='calculations.Section'),
        ),
        migrations.AddField(
            model_name='punching',
            name='support',
            field=models.ForeignKey(to='calculations.Support'),
        ),
    ]
