from django.test import TestCase, override_settings
from django.conf import global_settings
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from ipa.models import Word, Ipa, Audio

from tempfile import mkdtemp
from shutil import rmtree
from unittest.mock import MagicMock
import os

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
    @override_settings(DEFAULT_FILE_STORAGE=global_settings.DEFAULT_FILE_STORAGE)
    def test_audio_file_deleted_with_object(self):
        a = Audio()
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

