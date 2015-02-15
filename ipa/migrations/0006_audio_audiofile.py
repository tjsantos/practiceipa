# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ipa', '0005_rename_entry_to_word'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='audiofile',
            field=models.FileField(default=datetime.datetime(2015, 2, 15, 4, 21, 27, 108756, tzinfo=utc), upload_to=''),
            preserve_default=False,
        ),
    ]
