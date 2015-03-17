# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from os.path import basename

def set_filename(apps, schema_editor):
    Audio = apps.get_model('ipa', 'Audio')
    for audio in Audio.objects.all():
        audio.wiki_filename=basename(audio.audiofile.url)
        audio.save()

def reverse_set_filename(apps, schema_editor):
    Audio = apps.get_model('ipa', 'Audio')
    for audio in Audio.objects.all():
        audio.wiki_filename='default_filename'
        audio.save()

class Migration(migrations.Migration):

    dependencies = [
        ('ipa', '0010_accent_order_audio_ipa'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='wiki_filename',
            field=models.CharField(default='default_filename', max_length=100),
            preserve_default=False,
        ),
        migrations.RunPython(set_filename, reverse_set_filename),
    ]
