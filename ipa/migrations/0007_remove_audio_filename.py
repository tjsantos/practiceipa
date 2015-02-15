# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipa', '0006_audio_audiofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audio',
            name='filename',
        ),
    ]
