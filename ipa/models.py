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
    ('', 'Unspecified'),
    ('GB', 'British'),
    ('OT', 'Other'), # delete other?
)
# preserve order of accents for Ipa, Audio models
def accent_order(accent):
    order = {accent: i for i, (accent, _) in enumerate(ACCENTS)}
    if accent in order:
        return order[accent]
    else:
        return len(ACCENTS)

class Ipa(models.Model):
    ipa = models.CharField(max_length=200, db_index=True)
    accent = models.CharField(max_length=2, choices=ACCENTS, default='', blank=True)
    word = models.ForeignKey(Word)

    class Meta:
        order_with_respect_to = 'word'

    def save(self, *args, **kwargs):
        self.ipa = self.ipa.strip('/')
        super().save(*args, **kwargs)
        # order accents
        ipas = list(self.word.ipa_set.all())
        ipas.sort(key=lambda ipa: accent_order(ipa.accent))
        self.word.set_ipa_order([ipa.pk for ipa in ipas])

    def __str__(self):
        accent_tag = ' (GB)' if self.accent == 'GB' else ''
        return '/{}/{}'.format(self.ipa, accent_tag)

class Audio(models.Model):
    audiofile = models.FileField(upload_to='audio')
    accent = models.CharField(max_length=2, choices=ACCENTS, default='', blank=True)
    word = models.ForeignKey(Word)

    class Meta:
        order_with_respect_to = 'word'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # order by accent
        audios = list(self.word.audio_set.all())
        audios.sort(key=lambda audio: accent_order(audio.accent))
        self.word.set_audio_order([audio.pk for audio in audios])

    def delete(self, *args, **kwargs):
        '''Delete associated files'''
        self.audiofile.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.audiofile.url
