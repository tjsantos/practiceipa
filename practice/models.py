from django.db import models
from django.core.urlresolvers import reverse
from ipa.models import Word

class Wordlist(models.Model):
    name = models.CharField(max_length=200)
    words = models.ManyToManyField(Word)

    def get_absolute_url(self):
        name_in_url = self.name.replace(' ', '_')
        return reverse(
            'practice:wordlists', kwargs={'wordlist_id': self.id, 'wordlist_name': name_in_url}
        )
