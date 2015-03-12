# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipa', '0009_change_audiofile_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='accent',
            field=models.CharField(choices=[('US', 'American'), ('', 'Unspecified'), ('GB', 'British'), ('OT', 'Other')], default='', blank=True, max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ipa',
            name='accent',
            field=models.CharField(choices=[('US', 'American'), ('', 'Unspecified'), ('GB', 'British'), ('OT', 'Other')], default='', blank=True, max_length=2),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='audio',
            order_with_respect_to='word',
        ),
        migrations.AlterOrderWithRespectTo(
            name='ipa',
            order_with_respect_to='word',
        ),
    ]
