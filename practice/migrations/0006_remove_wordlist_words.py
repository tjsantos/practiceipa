# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0005_wordlist_words_1of3'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordlist',
            name='words',
        ),
    ]
