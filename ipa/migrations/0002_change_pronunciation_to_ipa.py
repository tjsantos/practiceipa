# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ipa',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('ipa', models.CharField(db_index=True, max_length=200)),
                ('accent', models.CharField(default='', max_length=2, choices=[('US', 'American'), ('UK', 'British'), ('OT', 'Other'), ('', 'Unspecified')])),
                ('entry', models.ForeignKey(to='ipa.Entry')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='pronunciation',
            name='entry',
        ),
        migrations.DeleteModel(
            name='Pronunciation',
        ),
    ]
