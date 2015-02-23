from django.test import TestCase
from practice.models import Wordlist
from django.core.urlresolvers import reverse, resolve

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
            wordlist.words.create(word=word)

        response = self.client.get(wordlist.get_absolute_url())
        for word in words:
            self.assertContains(response, word)
