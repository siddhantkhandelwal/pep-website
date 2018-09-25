# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-25 04:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_abstract_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstract',
            name='staff',
        ),
        migrations.AddField(
            model_name='abstract',
            name='staff',
            field=models.ManyToManyField(to='main.StaffProfile'),
        ),
    ]
