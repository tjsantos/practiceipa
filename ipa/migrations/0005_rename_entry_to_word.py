# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipa', '0004_allow_blank_accents'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Entry',
            new_name='Word',
        ),
        migrations.RenameField(
            model_name='audio',
            old_name='entry',
            new_name='word',
        ),
        migrations.RenameField(
            model_name='ipa',
            old_name='entry',
            new_name='word',
        ),
        migrations.RenameField(
            model_name='word',
            old_name='entry',
            new_name='word',
        ),
    ]
