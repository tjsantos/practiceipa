# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipa', '0002_change_pronunciation_to_ipa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('filename', models.CharField(max_length=100)),
                ('accent', models.CharField(default='', max_length=2, choices=[('US', 'American'), ('UK', 'British'), ('OT', 'Other'), ('', 'Unspecified')])),
                ('entry', models.ForeignKey(to='ipa.Entry')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
