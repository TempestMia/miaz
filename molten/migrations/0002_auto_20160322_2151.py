# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('molten', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='room',
            new_name='world',
        ),
        migrations.RemoveField(
            model_name='message',
            name='visitor',
        ),
        migrations.AddField(
            model_name='message',
            name='handle',
            field=models.TextField(default='merp'),
            preserve_default=False,
        ),
    ]
