# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-23 18:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_supervisorprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstract',
            name='verdict',
            field=models.CharField(blank=True, choices=[('Abstract Selected', 'Abstract Selected'), ('Abstract Rejected', 'Abstract Rejected')], max_length=20, null=True),
        ),
    ]