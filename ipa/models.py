from django.db import models
from django.core.urlresolvers import reverse

class Word(models.Model):
    LANGUAGE_CHOICES = (('en', 'English'),)
    LANG_CODES = set(code for (code, language) in LANGUAGE_CHOICES)
    word = models.CharField(max_length=200, db_index=True)
    lang = 'en'

    def wiktionary_url(self):
        return '//{}.wiktionary.org/wiki/{}'.format(self.lang, self.word)

    def get_absolute_url(self):
        return reverse('ipa:detail', kwargs={'search': self.word, 'lang': self.lang})

    def matches_ipa(self, ipa):
        return bool(self.ipa_set.filter(ipa__exact=ipa))

    def __str__(self):
        return self.word


ACCENTS = (
    ('US', 'American'),
    ('GB', 'British'),
    ('OT', 'Other'),
    ('', 'Unspecified'),
)

class Ipa(models.Model):
    ipa = models.CharField(max_length=200, db_index=True)
    accent = models.CharField(max_length=2, choices=ACCENTS, default='', blank=True)
    word = models.ForeignKey(Word)

    def __str__(self):
        return '/{}/'.format(self.ipa)

class Audio(models.Model):
    audiofile = models.FileField(upload_to='audio')
    accent = models.CharField(max_length=2, choices=ACCENTS, default='', blank=True)
    word = models.ForeignKey(Word)

    def delete(self, *args, **kwargs):
        '''Delete associated files'''
        self.audiofile.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.audiofile.url
