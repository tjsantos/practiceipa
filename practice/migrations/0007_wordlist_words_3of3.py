# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0006_remove_wordlist_words'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wordlist',
            old_name='words2',
            new_name='words',
        ),
    ]
