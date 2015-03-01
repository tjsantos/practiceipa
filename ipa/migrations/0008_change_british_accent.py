# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipa', '0007_remove_audio_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='accent',
            field=models.CharField(max_length=2, choices=[('US', 'American'), ('GB', 'British'), ('OT', 'Other'), ('', 'Unspecified')], default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ipa',
            name='accent',
            field=models.CharField(max_length=2, choices=[('US', 'American'), ('GB', 'British'), ('OT', 'Other'), ('', 'Unspecified')], default='', blank=True),
            preserve_default=True,
        ),
    ]
