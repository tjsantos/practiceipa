# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0002_change_wordlist_name_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordlist',
            name='slug',
            field=models.SlugField(default='default-slug', db_index=False),
            preserve_default=False,
        ),
    ]
