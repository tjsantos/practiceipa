from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from ipa.models import Word

class Wordlist(models.Model):
    name = models.CharField(max_length=100)
    words = models.ManyToManyField(Word)

    def get_absolute_url(self):
        slug = slugify(self.name)
        return reverse(
            'practice:wordlists', kwargs={'wordlist_id': self.id, 'wordlist_slug': slug}
        )
