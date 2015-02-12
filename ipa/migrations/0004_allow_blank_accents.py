# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipa', '0003_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='accent',
            field=models.CharField(default='', blank=True, max_length=2, choices=[('US', 'American'), ('UK', 'British'), ('OT', 'Other'), ('', 'Unspecified')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ipa',
            name='accent',
            field=models.CharField(default='', blank=True, max_length=2, choices=[('US', 'American'), ('UK', 'British'), ('OT', 'Other'), ('', 'Unspecified')]),
            preserve_default=True,
        ),
    ]
