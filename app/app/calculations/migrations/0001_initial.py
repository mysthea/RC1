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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('type', models.CharField(verbose_name='klasa', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DesignSituation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('type', models.CharField(verbose_name='typ', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Diametersw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('value', models.IntegerField(verbose_name='wartość')),
            ],
        ),
        migrations.CreateModel(
            name='Punching',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('b', models.DecimalField(max_digits=4, decimal_places=1)),
                ('h', models.DecimalField(max_digits=4, decimal_places=1)),
                ('dx', models.DecimalField(max_digits=4, decimal_places=1)),
                ('dy', models.DecimalField(max_digits=4, decimal_places=1)),
                ('lx', models.DecimalField(max_digits=4, decimal_places=1)),
                ('ly', models.DecimalField(max_digits=4, decimal_places=1)),
                ('ad', models.DecimalField(max_digits=3, decimal_places=1)),
                ('lambda_u', models.IntegerField()),
                ('asx', models.DecimalField(max_digits=3, decimal_places=1)),
                ('asy', models.DecimalField(max_digits=3, decimal_places=1)),
                ('ved', models.DecimalField(max_digits=5, decimal_places=1)),
                ('beta', models.DecimalField(max_digits=3, decimal_places=2)),
                ('vrdc', models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=3)),
                ('vrdmax', models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=3)),
                ('c_class', models.ForeignKey(to='calculations.Concrete')),
                ('design_situation', models.ForeignKey(to='calculations.DesignSituation')),
                ('dsw', models.ForeignKey(to='calculations.Diametersw')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('type', models.CharField(verbose_name='typ', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Steel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('type', models.CharField(verbose_name='klasa', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
            name='section',
            field=models.ForeignKey(to='calculations.Section'),
        ),
        migrations.AddField(
            model_name='punching',
            name='support',
            field=models.ForeignKey(to='calculations.Support'),
        ),
    ]
