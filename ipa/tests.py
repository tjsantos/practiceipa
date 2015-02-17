from django.test import TestCase
from django.conf import global_settings
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from ipa.models import Word, Ipa, Audio

from tempfile import mkdtemp
from shutil import rmtree
import os

# Create your tests here.

class WordViewTest(TestCase):

    def test_raises_404_on_invalid_lang_parameter(self):
        self.skipTest('TODO')

    def test_links_to_wiktionary_if_word_not_found(self):
        self.skipTest('TODO')

    def test_can_see_pronunciation_details(self):
        word = 'test'
        lang = 'en'
        ipas = ['ipa1', 'ipa2']
        word = Word.objects.create(word=word)
        for ipa in ipas:
            Ipa.objects.create(ipa=ipa, word=word)

        response = self.client.get(reverse('ipa:detail', args=(lang, word.word)))
        self.assertContains(response, word.word)
        for ipa in ipas:
            self.assertContains(response, ipa)

        # assert links to wiktionary

    #def test_can_see_audio_info(self):
    #    word = 'test'
    #    lang = 'en'
    #    audio_filename = 'boom.ogg'
    #    word = Word.objects.create(word=word)
    #    audio = Audio.objects.create(filename=audio_filename, word=word)

    #    response = self.client.get(reverse('detail', args=(lang, word.word)))
    #    self.assertContains(response, audio_filename)
    #    # ensure embed isn't escaped
    #    self.assertNotContains(response, 'src=&quot;')

class AudioModelTest(TestCase):

    # don't connect to external file storage
    def test_audio_file_deleted_with_object(self):
        a = Audio()
        # make sure file storage is default local and not external
        self.assertIn(global_settings.DEFAULT_FILE_STORAGE, str(a.audiofile.storage))

        word = Word.objects.create(word='abc')
        a.word = word
        try:
            folder = mkdtemp()
            with self.settings(MEDIA_ROOT=folder):
                a.audiofile.save('asdf', ContentFile('something'))
                self.assertEqual(1, len(os.listdir(folder)))
                # deleting the object should delete the associated file
                a.delete()
                self.assertEqual(0, len(os.listdir(folder)))
        finally:
            rmtree(folder)
            # TODO: `with` block for temp folders?

class SearchTest(TestCase):

    def test_search_raises_404_if_missing_get_parameter(self):
        response = self.client.get(reverse('ipa:search'), {'search': 'asdf'})
        self.assertEqual(404, response.status_code)

    def test_search_redirects_to_detail_given_parameters(self):
        response = self.client.get(reverse('ipa:search'), {'search': 'asdf', 'lang':'xqz'})
        self.assertRedirects(response, reverse('ipa:detail', args=('xqz', 'asdf')))
