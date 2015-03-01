# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipa', '0008_change_british_accent'),
        ('practice', '0004_migrate_slug_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordlistWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('word', models.ForeignKey(to='ipa.Word')),
                ('wordlist', models.ForeignKey(related_name='wordlist_words', to='practice.Wordlist')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('correct', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to='practice.SessionUser')),
                ('wordlist_word', models.ForeignKey(to='practice.WordlistWord')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='wordprogress',
            unique_together=set([('wordlist_word', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='wordlistword',
            unique_together=set([('wordlist', 'word')]),
        ),
        migrations.AddField(
            model_name='wordlist',
            name='words2',
            field=models.ManyToManyField(through='practice.WordlistWord', to='ipa.Word'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wordlist',
            name='words',
            field=models.ManyToManyField(related_name='to_delete', to='ipa.Word'),
            preserve_default=True,
        ),
    ]
