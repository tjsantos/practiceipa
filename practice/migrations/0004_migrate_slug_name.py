# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify

def set_slugs(apps, schema_editor):
    Wordlist = apps.get_model('practice', 'Wordlist')
    for wordlist in Wordlist.objects.all():
        # when saved, wordlist model sets slug based on name
        wordlist.slug = slugify(wordlist.name)[:50]
        wordlist.save()

def reverse_set_slugs(apps, schema_editor):
    Wordlist = apps.get_model('practice', 'Wordlist')
    for wordlist in Wordlist.objects.all():
        wordlist.slug = 'default-slug'
        wordlist.save()

class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0003_wordlist_slug'),
    ]

    operations = [
        migrations.RunPython(set_slugs, reverse_set_slugs),
    ]
