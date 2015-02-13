from django.test import TestCase
from django.core.urlresolvers import reverse
from ipa.models import Word, Ipa, Audio

# Create your tests here.

class WordViewTest(TestCase):

    def test_can_see_pronunciation_details(self):
        word = 'test'
        lang = 'en'
        ipas = ['ipa1', 'ipa2']
        word = Word.objects.create(word=word)
        for ipa in ipas:
            Ipa.objects.create(ipa=ipa, word=word)

        response = self.client.get(reverse('detail', args=(lang, word.word)))
        self.assertContains(response, word.word)
        for ipa in ipas:
            self.assertContains(response, ipa)

    def test_can_see_audio_info(self):
        word = 'test'
        lang = 'en'
        audio_filename = 'boom.ogg'
        word = Word.objects.create(word=word)
        audio = Audio.objects.create(filename=audio_filename, word=word)

        response = self.client.get(reverse('detail', args=(lang, word.word)))
        self.assertContains(response, audio_filename)
        # ensure embed isn't escaped
        self.assertNotContains(response, 'src=&quot;')
