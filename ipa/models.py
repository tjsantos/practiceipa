from django.db import models

# Create your models here.

class Word(models.Model):
    LANGUAGE_CHOICES = (('en', 'English'),)
    LANG_CODES = set(code for (code, language) in LANGUAGE_CHOICES)
    word = models.CharField(max_length=200, db_index=True)
    lang = 'en'

    def wiktionary_url(self):
        return '//{}.wiktionary.org/wiki/{}'.format(self.lang, self.word)


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

    def delete(self, *args, **kwargs):
        '''Delete associated files'''
        self.audiofile.delete()
        super().delete(*args, **kwargs)
