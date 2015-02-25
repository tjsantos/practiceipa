from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from ipa.models import Word

class Wordlist(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(db_index=False)
    words = models.ManyToManyField(Word)

    def get_absolute_url(self):
        return reverse(
            'practice:wordlists', kwargs={'wordlist_id': self.id, 'wordlist_slug': self.slug}
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:self._meta.get_field('slug').max_length]
        super().save(*args, **kwargs)
