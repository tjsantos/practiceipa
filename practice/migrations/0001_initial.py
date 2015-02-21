# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipa', '0007_remove_audio_filename'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wordlist',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('words', models.ManyToManyField(to='ipa.Word')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
