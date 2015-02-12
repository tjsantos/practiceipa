from django.db import models

# Create your models here.

class Entry(models.Model):
    entry = models.CharField(max_length=200, db_index=True)

ACCENTS = (
    ('US', 'American'),
    ('UK', 'British'),
    ('OT', 'Other'),
    ('', 'Unspecified'),
)

class Ipa(models.Model):
    ipa = models.CharField(max_length=200, db_index=True)
    accent = models.CharField(max_length=2, choices=ACCENTS, default='', blank=True)
    entry = models.ForeignKey(Entry)

class Audio(models.Model):
    filename = models.CharField(max_length=100)
    accent = models.CharField(max_length=2, choices=ACCENTS, default='', blank=True)
    entry = models.ForeignKey(Entry)

    def embed_html(self):
        return self.filename
