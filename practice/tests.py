from django.test import TestCase
from ipa.models import Word
from practice.models import Wordlist, WordlistWord
from django.core.urlresolvers import reverse, resolve
from django.utils.text import slugify

class WordlistViewTest(TestCase):

    def test_redirects_to_canonical_url(self):
        canonical_name = 'asdf'
        request_name = 'zxcv'
        wordlist = Wordlist.objects.create(name=canonical_name)
        response = self.client.get(reverse(
            'practice:wordlists', kwargs={'wordlist_id': wordlist.id, 'wordlist_slug': request_name}
        ))
        self.assertRedirects(response, wordlist.get_absolute_url())

    def test_wordlist_slug_with_spaces_has_valid_route(self):
        name = 'name with spaces'
        wordlist = Wordlist.objects.create(name=name)
        resolve(wordlist.get_absolute_url())

    def test_shows_words(self):
        wordlist = Wordlist.objects.create(name='healthy foods')
        words = ['apple', 'banana', 'carrot']
        for word in words:
            word_object = Word.objects.create(word=word)
            WordlistWord.objects.create(word=word_object, wordlist=wordlist)

        response = self.client.get(wordlist.get_absolute_url())
        for word in words:
            self.assertContains(response, word)

class WordlistModelTest(TestCase):

    def test_slugify_on_save(self):
        name = 'test i get slugified'
        wordlist = Wordlist.objects.create(name=name)
        self.assertEqual(slugify(name), wordlist.slug)
        # slug should be valid on name change
        # slug should truncate properly to max_length
        max_slug_length = Wordlist._meta.get_field('slug').max_length
        wordlist.name = 'a' * (1 + max_slug_length)
        wordlist.save()
        self.assertEqual('a' * max_slug_length, wordlist.slug)

class WordlistWordModelTest(TestCase):

    pass
