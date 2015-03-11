from django.core.management.base import BaseCommand, CommandError
import json
from ipa.models import Word, Ipa, Audio

class Command(BaseCommand):
    help = 'help text'

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def handle(self, *args, **options):
        json_words = {}
        for filename in args:
            with open(filename, 'r', encoding='utf-8') as f:
                more_json_words = json.load(f)
            json_words.update(more_json_words)
        import sys
        import codecs
        sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
        db_words = Word.objects.all()

        # delete words not present in load file
        for word_obj in db_words:
            if word_obj.word not in json_words:
                print('deleting {}'.format(word_obj));
                # call custom delete method to delete associated audio files
                for audio in word_obj.audio_set.all():
                    audio.delete()
                word_obj.delete()

        for word, info in json_words.items():
            word_obj, created = Word.objects.get_or_create(word=word)
            if created:
                print('created {}'.format(word_obj))
            if 'ipa' in info:
                ipas = set()
                for i_info in info['ipa']:
                    ipas.add((i_info['ipa'].strip('/'), i_info['accent']))
                # delete ipa not present in load file
                for ipa_obj in word_obj.ipa_set.all():
                    if (ipa_obj.ipa, ipa_obj.accent) not in ipas:
                        ipa_obj.delete()

                for ipa, accent in ipas:
                    Ipa.objects.get_or_create(word=word_obj, ipa=ipa, accent=accent)
