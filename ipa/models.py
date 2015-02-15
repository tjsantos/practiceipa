from django.db import models

# Create your models here.

class Word(models.Model):
    word = models.CharField(max_length=200, db_index=True)

ACCENTS = (
    ('US', 'American'),
    ('UK', 'British'),
    ('OT', 'Other'),
    ('', 'Unspecified'),
)

class Ipa(models.Model):
    ipa = models.CharField(max_length=200, db_index=True)
    accent = models.CharField(max_length=2, choices=ACCENTS, default='', blank=True)
    word = models.ForeignKey(Word)

class Audio(models.Model):
    audiofile = models.FileField()
    accent = models.CharField(max_length=2, choices=ACCENTS, default='', blank=True)
    word = models.ForeignKey(Word)
