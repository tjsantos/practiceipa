# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipa', '0008_change_british_accent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='audiofile',
            field=models.FileField(upload_to='audio'),
            preserve_default=True,
        ),
    ]
