# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-25 03:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20180921_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile'),
        ),
    ]
