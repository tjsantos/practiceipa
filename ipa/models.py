from django.db import models

# Create your models here.

class Entry(models.Model):
    entry = models.CharField(max_length=200, db_index=True)

class Pronunciation(models.Model):
    entry = models.ForeignKey(Entry)
    ipa = models.CharField(max_length=200)
