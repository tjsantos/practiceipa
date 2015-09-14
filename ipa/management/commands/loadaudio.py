from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from ipa.models import Word, Ipa, Audio

from ._downloader import WikimediaDownloader

import json
from os.path import basename
from time import strftime
from collections import defaultdict

class Command(BaseCommand):
    help = 'help text'

    def add_arguments(self, parser):
        parser.add_argument('filenames', nargs='+')

    def handle(self, *args, **options):
        json_words = {}
        for filename in options['filenames']:
            with open(filename, 'r', encoding='utf-8') as f:
                more_json_words = json.load(f)
            json_words.update(more_json_words)
        audio_to_words = defaultdict(list)
        for word, info in json_words.items():
            if 'audio' in info:
                for a_info in info['audio']:
                    filename = a_info['filename']
                    accent = a_info['accent']
                    audio_to_words[(filename, accent)].append(word)

        # sync audio currently in database to loaded audio data
        db_audio = Audio.objects.all().select_related('word')
        for audio in db_audio:
            filename = audio.wiki_filename
            accent = audio.accent
            if (filename, accent) not in audio_to_words:
                # delete audio not present in load file
                print('deleting {}'.format(audio))
                audio.delete()
            else:
                # update audio's word if it doesn't match
                try:
                    idx = audio_to_words[(filename, accent)].index(audio.word.word)
                except ValueError:
                    old_word_obj = audio.word
                    new_audio_word = audio_to_words[(filename, accent)].pop()
                    new_word_obj, created = Word.objects.get_or_create(word=new_audio_word)
                    audio.word = new_word_obj
                    audio.save()
                    print('changed word for {audio}: {old} -> {new}'.format(
                        audio=audio, old=old_word_obj, new=new_word_obj
                    ))
                else:
                    audio_to_words[(filename, accent)].pop(idx)
                finally:
                    # delete from dict when all words processed for a given wikimedia audio file
                    if not audio_to_words[(filename, accent)]:
                        audio_to_words.pop((filename, accent))

        # add new audio that was not yet present in database
        downloader = WikimediaDownloader()
        for (filename, accent), words in audio_to_words.items():
            for word in words:
                word_obj, created = Word.objects.get_or_create(word=word)
                audio = Audio(word=word_obj, accent=accent, wiki_filename=filename)
                print('downloading {}... '.format(filename), end='')
                # download and save file
                audiofile_bytes = downloader.download(filename)
                print('saving... ', end='')
                audio.audiofile.save(filename, ContentFile(audiofile_bytes))
                print(strftime('done %M:%S'))

