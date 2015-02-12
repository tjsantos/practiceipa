from django.test import TestCase
from django.core.urlresolvers import reverse
from ipa.models import Entry, Ipa

# Create your tests here.

class EntryViewTest(TestCase):

    def test_can_see_pronunciation_details(self):
        word = 'test'
        lang = 'en'
        ipas = ['ipa1', 'ipa2']
        entry = Entry.objects.create(entry=word)
        for ipa in ipas:
            Ipa.objects.create(ipa=ipa, entry=entry)

        response = self.client.get(reverse('detail', args=(lang, word)))
        self.assertContains(response, word)
        for ipa in ipas:
            self.assertContains(response, ipa)
